from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class QualityEvaluation(Base):
    __tablename__ = "quality_evaluations"
    id = Column(Integer, primary_key=True, index=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    inspection_date = Column(DateTime, default=datetime.utcnow)
    material_quality = Column(Integer, nullable=False)
    packaging_quality = Column(Integer, nullable=False)
    quantity_accuracy = Column(Integer, nullable=False)
    specification_compliance = Column(Integer, nullable=False)
    defect_count = Column(Integer, default=0)
    overall_rating = Column(Float, nullable=False)
    remarks = Column(String(255), nullable=True)
