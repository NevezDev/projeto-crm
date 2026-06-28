from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth_utils
from database import get_db
from models.task import Task
from models.user import User
from schemas.task_schema import TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/tasks")


@router.get("", response_model=None)
def listar(db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    return db.query(Task).filter(Task.user_id == current_user.id).all()


@router.post("", response_model=None)
def criar(dados: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    novo = Task(**dados.model_dump())
    novo.user_id = current_user.id
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{id}", response_model=None)
@router.patch("/{id}", response_model=None)
def atualizar(id: int, dados: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    tarefa = db.query(Task).filter(Task.id == id, Task.user_id == current_user.id).first()
    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa nao encontrada")

    for key, value in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, key, value)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{id}", response_model=None)
def deletar(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_utils.get_current_user)):
    tarefa = db.query(Task).filter(Task.id == id, Task.user_id == current_user.id).first()
    if not tarefa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa nao encontrada")

    db.delete(tarefa)
    db.commit()
    return {"msg": "deletada"}
