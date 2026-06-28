from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import auth_utils
from database import get_db
from models.company import Company
from models.contact import Contact
from models.deal import Deal
from models.user import User
from schemas.company_schema import CompanyCreate

router = APIRouter(prefix="/api/companies")


@router.get("", response_model=None)
def listar(db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    results = []

    for co in companies:
        contacts_count = db.query(func.count(Contact.id)).filter(
            Contact.company == co.name,
            Contact.user_id == current_user.id,
        ).scalar()
        contacts_names = db.query(Contact.name).filter(
            Contact.company == co.name,
            Contact.user_id == current_user.id,
        ).all()
        name_list = [name[0] for name in contacts_names]

        if name_list:
            deals_query = db.query(
                func.count(Deal.id).label("count"),
                func.sum(Deal.value).label("revenue"),
            ).filter(
                Deal.contact_name.in_(name_list),
                Deal.user_id == current_user.id,
            ).first()
        else:
            deals_query = (0, 0)

        results.append({
            "id": co.id,
            "name": co.name,
            "sector": co.sector,
            "contacts_count": contacts_count or 0,
            "deals_count": deals_query[0] or 0,
            "total_revenue": float(deals_query[1] or 0),
        })

    return results


@router.post("", response_model=None)
def criar(dados: CompanyCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    existente = db.query(Company).filter(
        Company.user_id == current_user.id,
        Company.name == dados.name,
    ).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Empresa ja cadastrada")

    nova = Company(**dados.model_dump())
    nova.user_id = current_user.id
    db.add(nova)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Empresa ja cadastrada")
    db.refresh(nova)
    return nova


@router.delete("/{id}", response_model=None)
def deletar(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    empresa = db.query(Company).filter(Company.id == id, Company.user_id == current_user.id).first()
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa nao encontrada")

    db.delete(empresa)
    db.commit()
    return {"msg": "Empresa deletada"}
