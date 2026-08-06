from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse
from app.services import purchase_order_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
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
    return purchase_order_service.get_all_purchase_orders(db)


@router.get("/vendor/{vendor_id}", response_model=List[PurchaseOrderResponse])
def pos_by_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
    return po


@router.put("/{po_id}/status")
def update_status(
    po_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER, Roles.VENDOR]))
):
    po = purchase_order_service.update_purchase_order_status(db, po_id, status)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return {"message": "Purchase Order status updated", "status": po.status}
