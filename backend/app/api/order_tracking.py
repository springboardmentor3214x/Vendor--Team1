from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.schemas.order_tracking import OrderTrackingResponse, OrderTrackingUpdate
from app.services import order_tracking_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/order-tracking", tags=["Order Tracking"])


@router.get("/", response_model=List[OrderTrackingResponse])
def list_tracking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_tracking_service.get_all_tracking(db)


@router.get("/{po_id}", response_model=OrderTrackingResponse)
def get_tracking(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tracking = order_tracking_service.get_tracking_by_po(db, po_id)
    if not tracking:
        raise HTTPException(status_code=404, detail="Order tracking not found for this Purchase Order")
    return tracking


@router.put("/{po_id}", response_model=OrderTrackingResponse)
def update_tracking(
    po_id: int,
    data: OrderTrackingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.SUPPLY_CHAIN_MANAGER, Roles.PROCUREMENT_MANAGER, Roles.VENDOR]))
):
    updated = order_tracking_service.update_tracking_status(db, po_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return updated
