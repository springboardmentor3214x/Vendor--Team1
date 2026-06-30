from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base

class Discussion(Base):
    __tablename__ = "discussions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=True)
