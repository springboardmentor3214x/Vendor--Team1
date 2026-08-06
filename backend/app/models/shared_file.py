from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base


class SharedFile(Base):
    __tablename__ = "shared_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)  # in bytes
    uploaded_by = Column(String(100), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True)
    discussion_id = Column(Integer, ForeignKey("discussions.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
