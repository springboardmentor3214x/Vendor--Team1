from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    certification_name = Column(String(150), nullable=False)
    certificate_number = Column(String(100), nullable=False)
    issuing_authority = Column(String(150), nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    status = Column(String(50), default="Active")  # Active, Expiring Soon, Expired
    file_name = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now())
