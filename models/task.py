from sqlalchemy import Column, Date, ForeignKey, Integer, String

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    related = Column(String)
    priority = Column(String)
    due_date = Column(Date)
    status = Column(String)
    notes = Column(String)
