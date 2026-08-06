from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    user_name = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    module_name = Column(String(100), nullable=False)
    related_record = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)
    details = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=func.now())
