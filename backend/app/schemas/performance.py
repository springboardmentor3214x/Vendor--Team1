from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeliveryPerformanceCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    expected_date: datetime

class DeliveryPerformanceResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    expected_date: datetime
    actual_date: datetime

class QualityEvaluationCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    material_quality: int
    packaging_quality: int
    quantity_accuracy: int

class QualityEvaluationResponse(BaseModel):
    id: int
    procurement_id: int
    vendor_id: int
    material_quality: int
    packaging_quality: int
    quantity_accuracy: int

class CommunicationLogCreate(BaseModel):
    procurement_id: int
    vendor_id: int
    message_sent_time: datetime


def _pending_performance_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_performance_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_performance_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_performance_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
