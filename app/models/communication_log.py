from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from app.database.base import Base

class CommunicationLog(Base):
    __tablename__ = "communication_logs"
    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    message_sent_time = Column(DateTime, nullable=False)
    vendor_response_time = Column(DateTime, nullable=True)
    response_duration_hours = Column(Float, nullable=True)
    communication_status = Column(String(50), default="Pending")
    remarks = Column(String(255), nullable=True)
