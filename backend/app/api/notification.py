from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services import notification_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/", response_model=NotificationResponse, status_code=201)
def create_notification(
    data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notification_service.create_notification(db, data)


@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    module: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    unread_only: bool = Query(False),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notification_service.get_user_notifications(
        db, current_user.id, current_user.role, module_name=module, priority=priority, unread_only=unread_only, limit=limit
    )


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notification_service.mark_notification_read(db, notification_id, current_user.id)


@router.put("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notification_service.mark_all_read(db, current_user.id, current_user.role)


@router.post("/trigger-background-checks")
def trigger_checks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return notification_service.trigger_background_expiry_and_delay_checks(db)
