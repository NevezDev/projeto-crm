from datetime import datetime, timezone

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Text

from database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    role = Column(String)
    company = Column(String)
    status = Column(String)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))
