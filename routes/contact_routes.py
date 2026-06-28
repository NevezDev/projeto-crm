from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth_utils
from database import get_db
from models.contact import Contact
from models.user import User
from schemas.contact_schema import ContactCreate

router = APIRouter(prefix="/api/contacts")


@router.get("", response_model=None)
def listar(db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    return db.query(Contact).filter(Contact.user_id == current_user.id).all()


@router.post("", response_model=None)
def criar(dados: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    novo = Contact(**dados.model_dump())
    novo.user_id = current_user.id
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{id}", response_model=None)
def atualizar(id: int, dados: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    contato = db.query(Contact).filter(Contact.id == id, Contact.user_id == current_user.id).first()
    if not contato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato nao encontrado")

    for key, value in dados.model_dump().items():
        setattr(contato, key, value)
    db.commit()
    return contato


@router.delete("/{id}", response_model=None)
def deletar(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    contato = db.query(Contact).filter(Contact.id == id, Contact.user_id == current_user.id).first()
    if not contato:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contato nao encontrado")

    db.delete(contato)
    db.commit()
    return {"msg": "Contato deletado"}
