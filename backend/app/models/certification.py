from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    certification_name = Column(String(150), nullable=False)
    certificate_number = Column(String(100), nullable=False)
