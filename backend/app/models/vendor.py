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

    # Extended Module 2 Profile Fields
    contact_person = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    alternate_phone = Column(String(20), nullable=True)
    gst_number = Column(String(50), nullable=True)
    pan_number = Column(String(50), nullable=True)
    company_registration_number = Column(String(50), nullable=True)
    address_line_1 = Column(String(255), nullable=True)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    pincode = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(String(500), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    payment_terms = Column(String(100), nullable=True)

    delivery_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    service_score = Column(Float, default=0.0)
    reliability_score = Column(Float, default=0.0)

    status = Column(String(50), default="Pending")
    approval_status = Column(String(50), default="Pending")
    approved_by = Column(String(100), nullable=True)
