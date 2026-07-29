from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.services import reliability_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, INTERNAL_ROLES
from app.core.vendor_scope import assert_owns
from app.models.user import User

router = APIRouter(prefix="/reliability", tags=["Vendor Reliability"])

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return reliability_service.get_reliability_dashboard(db)

@router.get("/details/{vendor_id}")
def get_details(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assert_owns(db, current_user, vendor_id, "reliability information")
    details = reliability_service.get_vendor_reliability_details(db, vendor_id)
    if not details:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return details


def _pending_reliability_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_reliability_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
