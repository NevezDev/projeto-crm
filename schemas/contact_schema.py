from typing import Optional

from pydantic import BaseModel


class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    role: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = "lead"
    notes: Optional[str] = None


class ContactResponse(ContactCreate):
    id: int

    class Config:
        from_attributes = True
