from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from app.database.base import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contract_title = Column(String(100), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    vendor_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    contract_value = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default="Active")
