from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationCreate(BaseModel):
    user_id: Optional[int] = None
    target_role: Optional[str] = None
    notification_type: str
    title: str
    description: str
    module_name: str
    related_record_id: Optional[str] = None
    priority: Optional[str] = "Medium"
    delivery_method: Optional[str] = "In-App"


class NotificationResponse(NotificationCreate):
    id: int
    is_read: bool = False
    email_sent: bool = False
    sms_sent: bool = False
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
