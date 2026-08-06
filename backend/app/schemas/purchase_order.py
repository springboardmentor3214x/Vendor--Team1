from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PurchaseOrderCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    vendor_name: str
    vendor_address: Optional[str] = None
    contact_person: Optional[str] = None
    item_name: str
    quantity: int
    unit_price: float
    tax_amount: Optional[float] = 0.0
    shipping_address: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    payment_terms: Optional[str] = None


class PurchaseOrderUpdate(BaseModel):
    status: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    payment_terms: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderCreate):
    id: int
    po_number: str
    total_cost: float
    status: str
    approved_by: Optional[str] = None
    po_date: datetime

    class Config:
        from_attributes = True
