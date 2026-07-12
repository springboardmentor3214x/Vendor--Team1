from sqlalchemy import Column, Float, Integer, String
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
    
    delivery_score = Column(Integer, default=0)

    quality_score = Column(Integer, default=0)

    compliance_score = Column(Integer, default=0)

    communication_score = Column(Integer, default=0)

    reliability_score = Column(Float, default=0)

    status = Column(
        String(50),
        default="Pending"
    )

    # New Fields
    approval_status = Column(
        String(50),
        default="Pending"
    )

    approved_by = Column(
        String(100),
        nullable=True
    )