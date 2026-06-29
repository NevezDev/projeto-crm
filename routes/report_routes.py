from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import auth_utils
from database import get_db
from models.contact import Contact
from models.deal import Deal
from models.user import User

router = APIRouter(prefix="/api/reports")


@router.get("/summary", response_model=None)
def resumo(db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    contatos = db.query(func.count(Contact.id)).filter(Contact.user_id == current_user.id).scalar()
    deals_count = db.query(func.count(Deal.id)).filter(Deal.user_id == current_user.id).scalar()
    receita = db.query(func.coalesce(func.sum(Deal.value), 0)).filter(Deal.user_id == current_user.id).scalar()

    funnel_data = db.query(
        Deal.stage,
        func.count(Deal.id),
    ).filter(Deal.user_id == current_user.id).group_by(Deal.stage).all()
    funnel = {stage: count for stage, count in funnel_data}

    recent_contacts = db.query(Contact).filter(
        Contact.user_id == current_user.id,
    ).order_by(Contact.created_at.desc()).limit(3).all()

    activities = []
    for contact in recent_contacts:
        activities.append({
            "icon": "fa-user-plus",
            "cls": "green",
            "contact_name": contact.name,
            "action": "foi adicionado como novo contato",
            "time": "Recentemente",
        })

    return {
        "contacts_total": contatos,
        "deals_active": deals_count,
        "pipeline_revenue": receita,
        "conversion_rate": 0,
        "funnel": funnel,
        "activities": activities,
    }
