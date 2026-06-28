from datetime import date
from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    related: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[date] = None
    status: Optional[str] = "pending"
    notes: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    related: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None
