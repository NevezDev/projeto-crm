from datetime import date

from pydantic import BaseModel, Field


class DealCreate(BaseModel):
    title: str
    contact_name: str
    stage: str
    value: float
    close_date: date
    probability: int = Field(ge=0, le=100)
