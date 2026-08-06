from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base


class Discussion(Base):
    __tablename__ = "discussions"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True)
    created_by = Column(String(100), nullable=False)
    status = Column(String(50), default="Active")  # Active, Resolved, Closed
    created_at = Column(DateTime, default=func.now())
