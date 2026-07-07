from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    reliability_score = Column(Float)

    risk_level = Column(String)

    remarks = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)