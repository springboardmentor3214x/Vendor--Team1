from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database.base import Base


class Communication(Base):
    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True)
    discussion_id = Column(Integer, nullable=True)
    sender_id = Column(Integer, nullable=True)
    sender_name = Column(String(100), nullable=False)
    receiver_id = Column(Integer, nullable=True)
    receiver_name = Column(String(100), nullable=True)
    message = Column(String(2000), nullable=False)
    is_read = Column(Boolean, default=False)
    file_name = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    sent_at = Column(DateTime, default=func.now())
