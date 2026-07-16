from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeliveryPerformanceCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    expected_date: datetime
    actual_date: datetime
    remarks: Optional[str] = None

class DeliveryPerformanceResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    expected_date: datetime
    actual_date: datetime
    delay_days: int
    delivery_status: str
    remarks: Optional[str]
    class Config:
        from_attributes = True

class QualityEvaluationCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    material_quality: int
    packaging_quality: int
    quantity_accuracy: int
    specification_compliance: int
    defect_count: int = 0
    remarks: Optional[str] = None

class QualityEvaluationResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    material_quality: int
    packaging_quality: int
    quantity_accuracy: int
    specification_compliance: int
    defect_count: int
    overall_rating: float
    remarks: Optional[str]
    class Config:
        from_attributes = True
