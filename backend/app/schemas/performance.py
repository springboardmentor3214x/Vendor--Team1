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

class CommunicationLogCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    message_sent_time: datetime
    vendor_response_time: Optional[datetime] = None
    remarks: Optional[str] = None

class CommunicationLogResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    message_sent_time: datetime
    vendor_response_time: Optional[datetime]
    response_duration_hours: Optional[float]
    communication_status: str
    remarks: Optional[str]
    class Config:
        from_attributes = True

class ServiceRatingCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    professionalism: int
    customer_support: int
    documentation_quality: int
    flexibility: int
    communication_effectiveness: int
    issue_resolution: int
    comments: Optional[str] = None

class ServiceRatingResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    professionalism: int
    customer_support: int
    documentation_quality: int
    flexibility: int
    communication_effectiveness: int
    issue_resolution: int
    overall_rating: float
    comments: Optional[str]
    class Config:
        from_attributes = True
