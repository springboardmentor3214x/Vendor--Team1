from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.performance import (
    DeliveryPerformanceCreate, DeliveryPerformanceResponse,
    QualityEvaluationCreate, QualityEvaluationResponse,
    CommunicationLogCreate, CommunicationLogResponse,
    ServiceRatingCreate, ServiceRatingResponse
)
from app.services import performance_service

router = APIRouter(prefix="/performance", tags=["Vendor Performance"])

@router.post("/delivery", response_model=DeliveryPerformanceResponse, status_code=201)
def record_delivery(data: DeliveryPerformanceCreate, db: Session = Depends(get_db)):
    """Record delivery performance for a procurement."""
    return performance_service.record_delivery(db, data)

@router.get("/delivery/{vendor_id}", response_model=List[DeliveryPerformanceResponse])
def get_delivery(vendor_id: int, db: Session = Depends(get_db)):
    return performance_service.get_delivery_records(db, vendor_id)

@router.post("/quality", response_model=QualityEvaluationResponse, status_code=201)
def record_quality(data: QualityEvaluationCreate, db: Session = Depends(get_db)):
    """Submit product quality evaluation."""
    return performance_service.record_quality(db, data)

@router.get("/quality/{vendor_id}", response_model=List[QualityEvaluationResponse])
def get_quality(vendor_id: int, db: Session = Depends(get_db)):
    return performance_service.get_quality_records(db, vendor_id)

@router.post("/communication", response_model=CommunicationLogResponse, status_code=201)
def record_communication(data: CommunicationLogCreate, db: Session = Depends(get_db)):
    """Record vendor communication response."""
    return performance_service.record_communication(db, data)

@router.get("/communication/{vendor_id}", response_model=List[CommunicationLogResponse])
def get_communication(vendor_id: int, db: Session = Depends(get_db)):
    return performance_service.get_communication_records(db, vendor_id)

@router.post("/service-rating", response_model=ServiceRatingResponse, status_code=201)
def submit_rating(data: ServiceRatingCreate, db: Session = Depends(get_db)):
    """Submit overall service rating for a vendor."""
    return performance_service.submit_service_rating(db, data)

@router.get("/service-rating/{vendor_id}", response_model=List[ServiceRatingResponse])
def get_ratings(vendor_id: int, db: Session = Depends(get_db)):
    return performance_service.get_service_ratings(db, vendor_id)
