from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from database import Base


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    contact_name = Column(String)
    stage = Column(String)
    value = Column(Float)
    close_date = Column(Date)
    probability = Column(Integer)
