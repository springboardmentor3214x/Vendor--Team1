from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderTrackingResponse(BaseModel):
    id: int
    po_id: int
    procurement_id: int
    vendor_id: int
    dispatch_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    delivery_status: str
    delay_status: str
    delay_hours: int
    delay_days: int
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderTrackingUpdate(BaseModel):
    delivery_status: str
    dispatch_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
