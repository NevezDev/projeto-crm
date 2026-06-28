from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    sector: str
    contacts_count: int = 0
    deals_count: int = 0
    total_revenue: float = 0.0
