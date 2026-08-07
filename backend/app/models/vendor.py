from sqlalchemy import Column, Integer, String, Float
from app.database.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(100), nullable=False)
    company_name = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)

    delivery_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    service_score = Column(Float, default=0.0)
    reliability_score = Column(Float, default=0.0)

    status = Column(String(50), default="Pending")
    approval_status = Column(String(50), default="Pending")
    approved_by = Column(String(100), nullable=True)
