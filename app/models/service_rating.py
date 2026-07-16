from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class ServiceRating(Base):
    __tablename__ = "service_ratings"
    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    professionalism = Column(Integer, nullable=False)
    customer_support = Column(Integer, nullable=False)
    documentation_quality = Column(Integer, nullable=False)
    flexibility = Column(Integer, nullable=False)
    communication_effectiveness = Column(Integer, nullable=False)
    issue_resolution = Column(Integer, nullable=False)
    overall_rating = Column(Float, nullable=False)
    comments = Column(String(500), nullable=True)
    rated_at = Column(DateTime, default=datetime.utcnow)
