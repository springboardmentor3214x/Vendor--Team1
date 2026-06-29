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
