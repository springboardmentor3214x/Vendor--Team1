from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.order_tracking import OrderTrackingResponse, OrderTrackingUpdate
from app.services import order_tracking_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.core.vendor_scope import assert_owns, restrict_to_vendor
from app.models.user import User

router = APIRouter(prefix="/order-tracking", tags=["Order Tracking"])

@router.get("/", response_model=List[OrderTrackingResponse])
def list_tracking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return restrict_to_vendor(
        db, current_user,
        order_tracking_service.get_all_tracking(db),
        "order tracking records"
    )


def _pending_order_tracking_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_order_tracking_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_order_tracking_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows
