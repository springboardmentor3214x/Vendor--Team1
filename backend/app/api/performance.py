from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.performance import (
    DeliveryPerformanceCreate, DeliveryPerformanceResponse,
    QualityEvaluationCreate, QualityEvaluationResponse,
    CommunicationLogCreate, CommunicationLogResponse,
    ServiceRatingCreate, ServiceRatingResponse
)
from app.services import performance_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, INTERNAL_ROLES
from app.core.vendor_scope import assert_owns
from app.models.user import User

router = APIRouter(prefix="/performance", tags=["Vendor Performance"])

EVALUATOR_ROLES = [Roles.ADMIN, Roles.SUPPLY_CHAIN_MANAGER, Roles.PROCUREMENT_MANAGER]

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return performance_service.performance_dashboard(db)

@router.get("/metrics/{vendor_id}")
def vendor_metrics(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assert_owns(db, current_user, vendor_id, "performance data")
    return performance_service.calculate_vendor_metrics(db, vendor_id)

@router.get("/rankings")
def vendor_rankings(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return performance_service.generate_vendor_rankings(db)

@router.get("/history/{vendor_id}")
def vendor_history(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assert_owns(db, current_user, vendor_id, "performance data")
    return performance_service.get_vendor_performance_history(db, vendor_id)

@router.post("/delivery", response_model=DeliveryPerformanceResponse, status_code=201)
def record_delivery(
    data: DeliveryPerformanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(EVALUATOR_ROLES))
):
    return performance_service.record_delivery(db, data)

@router.get("/delivery/{vendor_id}", response_model=List[DeliveryPerformanceResponse])
def get_delivery(vendor_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    assert_owns(db, current_user, vendor_id, "delivery records")
    return performance_service.get_delivery_records(db, vendor_id)

@router.post("/quality", response_model=QualityEvaluationResponse, status_code=201)
def record_quality(
    data: QualityEvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(EVALUATOR_ROLES))
):
    return performance_service.record_quality(db, data)


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


def _pending_performance_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
