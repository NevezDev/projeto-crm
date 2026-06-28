from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routes import (
    auth_routes,
    company_routes,
    contact_routes,
    deal_routes,
    report_routes,
    task_routes,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Guia CRM API",
    description="API para um CRM simples com contatos, empresas, tarefas, negocios e relatorios.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact_routes.router)
app.include_router(deal_routes.router)
app.include_router(task_routes.router)
app.include_router(company_routes.router)
app.include_router(report_routes.router)
app.include_router(auth_routes.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
