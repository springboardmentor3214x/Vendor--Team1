from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class ComplianceRecord(Base):
    __tablename__ = "compliance_records"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    compliance_type = Column(String(100), nullable=False)  # GST, Tax, ISO, Environmental, Cybersecurity, Labor Laws
    status = Column(String(50), default="Pending Verification")  # Compliant, Pending Verification, Non-Compliant, Expired
    verified_by = Column(String(100), nullable=True)
    verification_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    remarks = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now())
