from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse
from app.services import purchase_order_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.core.vendor_scope import assert_owns, restrict_to_vendor
from app.models.user import User

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])

@router.post("/", response_model=PurchaseOrderResponse, status_code=201)
def create_po(
    data: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    return purchase_order_service.create_purchase_order(db, data, current_user.name)

@router.get("/", response_model=List[PurchaseOrderResponse])
def list_pos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return restrict_to_vendor(
        db, current_user,
        purchase_order_service.get_all_purchase_orders(db),
        "purchase orders"
    )

@router.get("/vendor/{vendor_id}", response_model=List[PurchaseOrderResponse])
def pos_by_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assert_owns(db, current_user, vendor_id, "purchase orders")
    return purchase_order_service.get_purchase_orders_by_vendor(db, vendor_id)

@router.get("/{po_id}", response_model=PurchaseOrderResponse)
def get_po(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    po = purchase_order_service.get_purchase_order(db, po_id)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    assert_owns(db, current_user, po.vendor_id, "purchase orders")
    return po


def _pending_purchase_order_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_purchase_order_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_purchase_order_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_purchase_order_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_purchase_order_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows
