import os
import unittest

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def register_and_login(self, email: str, name: str = "Usuario Teste") -> dict:
        register = self.client.post(
            "/api/auth/register",
            json={"full_name": name, "email": email, "password": "senha-segura"},
        )
        self.assertEqual(register.status_code, 201, register.text)

        login = self.client.post(
            "/api/auth/login",
            json={"email": email, "password": "senha-segura"},
        )
        self.assertEqual(login.status_code, 200, login.text)
        return {"Authorization": f"Bearer {login.json()['access_token']}"}

    def test_registration_validates_payload(self):
        response = self.client.post(
            "/api/auth/register",
            json={"full_name": "A", "email": "invalido", "password": "123"},
        )
        self.assertEqual(response.status_code, 422)

    def test_task_can_be_completed_with_partial_update(self):
        headers = self.register_and_login("tasks@example.com")
        created = self.client.post(
            "/api/tasks",
            headers=headers,
            json={
                "title": "Preparar proposta",
                "related": "Cliente A",
                "priority": "high",
                "due_date": "2026-07-10",
                "status": "pending",
                "notes": "Manter estes dados",
            },
        )
        self.assertEqual(created.status_code, 200, created.text)

        updated = self.client.patch(
            f"/api/tasks/{created.json()['id']}",
            headers=headers,
            json={"status": "done"},
        )
        self.assertEqual(updated.status_code, 200, updated.text)
        self.assertEqual(updated.json()["status"], "done")
        self.assertEqual(updated.json()["title"], "Preparar proposta")
        self.assertEqual(updated.json()["notes"], "Manter estes dados")

    def test_companies_are_unique_per_user(self):
        first_user = self.register_and_login("first@example.com", "Primeiro Usuario")
        second_user = self.register_and_login("second@example.com", "Segundo Usuario")
        company = {"name": "Acme", "sector": "Tecnologia"}

        first = self.client.post("/api/companies", headers=first_user, json=company)
        second = self.client.post("/api/companies", headers=second_user, json=company)
        duplicate = self.client.post("/api/companies", headers=first_user, json=company)

        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(second.status_code, 200, second.text)
        self.assertEqual(duplicate.status_code, 409, duplicate.text)

    def test_users_cannot_access_each_others_tasks(self):
        owner = self.register_and_login("owner@example.com")
        stranger = self.register_and_login("stranger@example.com")
        created = self.client.post(
            "/api/tasks",
            headers=owner,
            json={"title": "Tarefa privada"},
        )

        response = self.client.patch(
            f"/api/tasks/{created.json()['id']}",
            headers=stranger,
            json={"status": "done"},
        )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
