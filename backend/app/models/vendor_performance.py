from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class VendorPerformance(Base):
    __tablename__ = "vendor_performance"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    quality_score = Column(Float)

    delivery_score = Column(Float)

    cost_score = Column(Float)

    response_time = Column(Float)

    reliability_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)