from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    procurement_id = Column(Integer, ForeignKey("procurements.id"))

    po_number = Column(String, unique=True)

    order_date = Column(Date)

    delivery_date = Column(Date)

    amount = Column(Float)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)