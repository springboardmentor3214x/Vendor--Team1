from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.base import Base

class Communication(Base):
    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    sender = Column(String(100), nullable=False)
    message = Column(String(1000), nullable=False)
    sent_at = Column(DateTime, nullable=False)
