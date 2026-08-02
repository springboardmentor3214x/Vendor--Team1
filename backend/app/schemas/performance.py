from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeliveryPerformanceCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    expected_date: datetime
    actual_date: datetime

class DeliveryPerformanceResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    expected_date: datetime
    actual_date: datetime
    delay_days: int
    delivery_status: str

class QualityEvaluationCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    material_quality: int
    packaging_quality: int
    quantity_accuracy: int
    specification_compliance: int

class QualityEvaluationResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    material_quality: int
    packaging_quality: int
    quantity_accuracy: int
    specification_compliance: int
    defect_count: int

class CommunicationLogCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    message_sent_time: datetime
    vendor_response_time: Optional[datetime] = None

class CommunicationLogResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    message_sent_time: datetime
    vendor_response_time: Optional[datetime] = None
    response_duration_hours: Optional[float] = None
    communication_status: str


def _pending_performance_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_performance_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_performance_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_performance_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_performance_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows
