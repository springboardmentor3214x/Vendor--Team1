from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(50), unique=True, nullable=False)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    vendor_name = Column(String(150), nullable=False)
    vendor_address = Column(String(255), nullable=True)
    contact_person = Column(String(100), nullable=True)
    item_name = Column(String(150), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    shipping_address = Column(String(255), nullable=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    payment_terms = Column(String(100), nullable=True)
    status = Column(String(50), default="Issued") # Issued, In Transit, Delivered, Completed, Cancelled
    approved_by = Column(String(100), nullable=True)
    po_date = Column(DateTime, default=datetime.utcnow)
