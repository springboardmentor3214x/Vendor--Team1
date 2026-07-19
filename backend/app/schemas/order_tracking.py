from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime

DELIVERY_STATUSES = ["Awaiting Shipment", "In Transit", "Delivered", "Completed"]


class OrderTrackingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    po_id: int
    procurement_id: int
    vendor_id: int
    po_number: Optional[str] = None
    dispatch_date: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    delivery_status: str
    delay_status: str
    delay_hours: int
    delay_days: int
    updated_at: datetime


class OrderTrackingUpdate(BaseModel):
    delivery_status: str
    dispatch_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None

    @field_validator("delivery_status")
    @classmethod
    def status_allowed(cls, v: str) -> str:
        if v not in DELIVERY_STATUSES:
            raise ValueError(
                f"Invalid delivery status '{v}'. Allowed values: {', '.join(DELIVERY_STATUSES)}"
            )
        return v
