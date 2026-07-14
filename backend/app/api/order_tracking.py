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

@router.get("/{po_id}", response_model=OrderTrackingResponse)
def get_tracking(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tracking = order_tracking_service.get_tracking_by_po(db, po_id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Order tracking not found for this Purchase Order")
    assert_owns(db, current_user, tracking.vendor_id, "order tracking records")
    return tracking


def _pending_order_tracking_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_order_tracking_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_order_tracking_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
