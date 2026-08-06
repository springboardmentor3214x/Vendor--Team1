from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProcurementCreate(BaseModel):
    request_title: Optional[str] = None
    department: Optional[str] = None
    requested_by: Optional[str] = None
    item_name: str
    category: Optional[str] = None
    vendor_id: Optional[int] = None
    quantity: int
    unit_of_measurement: Optional[str] = None
    unit_price: float
    priority: Optional[str] = "Medium"
    business_justification: Optional[str] = None
    remarks: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None


class ProcurementResponse(BaseModel):
    id: int
    request_number: Optional[str] = None
    request_title: Optional[str] = None
    department: Optional[str] = None
    requested_by: Optional[str] = None
    item_name: str
    category: Optional[str] = None
    vendor_id: Optional[int] = None
    quantity: int
    unit_of_measurement: Optional[str] = None
    unit_price: float
    total_price: float
    priority: Optional[str] = "Medium"
    business_justification: Optional[str] = None
    remarks: Optional[str] = None
    status: str
    approval_status: str
    approved_by: Optional[str] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
