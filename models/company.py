from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint

from database import Base


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_company_user_name"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    sector = Column(String)
    contacts_count = Column(Integer, default=0)
    deals_count = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
