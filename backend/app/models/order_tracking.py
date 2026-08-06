from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base


class OrderTracking(Base):
    __tablename__ = "order_tracking"

    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    dispatch_date = Column(DateTime, nullable=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    delivery_status = Column(String(50), default="Awaiting Shipment") # Awaiting Shipment, In Transit, Delivered, Delayed, Completed
    delay_status = Column(String(50), default="On Time") # On Time, Delayed
    delay_hours = Column(Integer, default=0)
    delay_days = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
