from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base


class Procurement(Base):
    __tablename__ = "procurements"

    id = Column(Integer, primary_key=True, index=True)
    request_number = Column(String(50), unique=True, nullable=True)
    request_title = Column(String(150), nullable=True)
    department = Column(String(100), nullable=True)
    requested_by = Column(String(100), nullable=True)
    item_name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_of_measurement = Column(String(50), nullable=True)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    priority = Column(String(20), default="Medium")
    business_justification = Column(String(500), nullable=True)
    remarks = Column(String(500), nullable=True)
    status = Column(String(50), default="Pending")
    approval_status = Column(String(50), default="Pending")
    approved_by = Column(String(100), nullable=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
