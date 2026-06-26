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
