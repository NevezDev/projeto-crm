from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import auth_utils
from database import get_db
from models.deal import Deal
from models.user import User
from schemas.deal_schema import DealCreate

router = APIRouter(prefix="/api/deals")


@router.get("", response_model=None)
def listar(db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    return db.query(Deal).filter(Deal.user_id == current_user.id).all()


@router.post("", response_model=None)
def criar(dados: DealCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    novo = Deal(**dados.model_dump())
    novo.user_id = current_user.id
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{id}", response_model=None)
def atualizar(id: int, dados: DealCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    obj = db.query(Deal).filter(Deal.id == id, Deal.user_id == current_user.id).first()
    if not obj:
        return {"error": "Negocio nao encontrado"}

    for key, value in dados.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", response_model=None)
def deletar(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    obj = db.query(Deal).filter(Deal.id == id, Deal.user_id == current_user.id).first()
    if not obj:
        return {"error": "Negocio nao encontrado"}

    db.delete(obj)
    db.commit()
    return {"msg": "deletado"}
