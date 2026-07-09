from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcurementCreate(BaseModel):
    item_name: str
    vendor_id: int
    quantity: int
    unit_price: float

class ProcurementResponse(BaseModel):
    id: int
    item_name: str
    vendor_id: int
    quantity: int
    unit_price: float
    total_price: float
    status: str
    class Config:
        from_attributes = True
