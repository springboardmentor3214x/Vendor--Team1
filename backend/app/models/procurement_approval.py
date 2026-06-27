from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class ProcurementApproval(Base):
    __tablename__ = "procurement_approvals"
    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    action = Column(String(50), nullable=False)
