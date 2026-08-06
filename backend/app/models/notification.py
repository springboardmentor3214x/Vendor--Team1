from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_role = Column(String(50), nullable=True)
    notification_type = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    module_name = Column(String(100), nullable=False)
    related_record_id = Column(String(100), nullable=True)
    priority = Column(String(20), default="Medium")  # High, Medium, Low
    delivery_method = Column(String(50), default="In-App")  # In-App, Email, SMS, All
    is_read = Column(Boolean, default=False)
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=func.now())
