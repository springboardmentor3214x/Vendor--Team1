from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base

class Communication(Base):
    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, nullable=False)
    sender = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    sent_at = Column(DateTime, nullable=False)
