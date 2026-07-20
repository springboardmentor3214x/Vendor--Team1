from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class DeliveryPerformance(Base):
    __tablename__ = "delivery_performances"
    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    expected_date = Column(DateTime, nullable=False)
    actual_date = Column(DateTime, nullable=False)
    delay_days = Column(Integer, default=0)
    delivery_status = Column(String(50), nullable=False)
    remarks = Column(String(255), nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
