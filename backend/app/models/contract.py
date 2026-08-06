from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), unique=True, index=True, nullable=True)
    contract_title = Column(String(150), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    vendor_name = Column(String(100), nullable=False)
    contract_type = Column(String(50), default="Master Agreement")
    procurement_category = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    contract_value = Column(Float, nullable=False, default=0.0)
    payment_terms = Column(String(100), default="Net 30")
    sla_details = Column(String(500), nullable=True)
    warranty_details = Column(String(500), nullable=True)
    responsible_manager = Column(String(100), nullable=True)
    status = Column(String(50), default="Active")  # Draft, Active, Expiring Soon, Expired, Renewed, Terminated
    document_name = Column(String(255), nullable=True)
    document_path = Column(String(500), nullable=True)
    renewal_count = Column(Integer, default=0)
    last_renewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
