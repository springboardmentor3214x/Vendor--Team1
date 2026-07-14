from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcurementCreate(BaseModel):
    item_name: str
    vendor_id: int
    quantity: int
    unit_price: float
    expected_delivery_date: Optional[datetime] = None

class ProcurementResponse(BaseModel):
    id: int
    item_name: str
    vendor_id: int
    quantity: int
    unit_price: float
    total_price: float
    status: str
    approval_status: str
    approved_by: Optional[str]
    expected_delivery_date: Optional[datetime]
    actual_delivery_date: Optional[datetime]
    class Config:
        from_attributes = True
