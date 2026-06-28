from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth_utils
from database import get_db
from models.user import User
from schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/api/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
def registrar(user_data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=auth_utils.get_password_hash(user_data.password),
    )
    db.add(new_user)
    db.commit()
    return {"msg": "Usuario cadastrado com sucesso!"}


@router.post("/login", response_model=TokenResponse)
def logar(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not auth_utils.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha invalidos")

    access_token = auth_utils.create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"name": user.full_name, "email": user.email},
    }
