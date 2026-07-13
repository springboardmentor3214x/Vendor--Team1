from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.schemas.performance import (
    DeliveryPerformanceCreate, QualityEvaluationCreate,
    CommunicationLogCreate, ServiceRatingCreate
)

# ===== Delivery Performance =====
def record_delivery(db: Session, data: DeliveryPerformanceCreate):
    delta = (data.actual_date - data.expected_date).days
    delay_days = max(delta, 0)
    if delta < 0:
        status = "Early Delivery"
    elif delta == 0:
        status = "On-Time Delivery"
    else:
        status = "Delayed Delivery"
    record = DeliveryPerformance(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        expected_date=data.expected_date, actual_date=data.actual_date,
        delay_days=delay_days, delivery_status=status, remarks=data.remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_delivery_records(db: Session, vendor_id: int):
    return db.query(DeliveryPerformance).filter(DeliveryPerformance.vendor_id == vendor_id).all()

# ===== Quality Evaluation =====
def record_quality(db: Session, data: QualityEvaluationCreate):
    overall = (data.material_quality + data.packaging_quality + data.quantity_accuracy + data.specification_compliance) / 4.0
    record = QualityEvaluation(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        material_quality=data.material_quality, packaging_quality=data.packaging_quality,
        quantity_accuracy=data.quantity_accuracy, specification_compliance=data.specification_compliance,
        defect_count=data.defect_count, overall_rating=round(overall, 2), remarks=data.remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_quality_records(db: Session, vendor_id: int):
    return db.query(QualityEvaluation).filter(QualityEvaluation.vendor_id == vendor_id).all()

# ===== Communication Log =====
def record_communication(db: Session, data: CommunicationLogCreate):
    duration = None
    status = "Pending"
    if data.vendor_response_time:
        delta = data.vendor_response_time - data.message_sent_time
        duration = round(delta.total_seconds() / 3600, 2)
        status = "Responded"
    record = CommunicationLog(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        message_sent_time=data.message_sent_time, vendor_response_time=data.vendor_response_time,
        response_duration_hours=duration, communication_status=status, remarks=data.remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_communication_records(db: Session, vendor_id: int):
    return db.query(CommunicationLog).filter(CommunicationLog.vendor_id == vendor_id).all()

# ===== Service Rating =====
def submit_service_rating(db: Session, data: ServiceRatingCreate):
    overall = (data.professionalism + data.customer_support + data.documentation_quality + data.flexibility + data.communication_effectiveness + data.issue_resolution) / 6.0
    record = ServiceRating(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        professionalism=data.professionalism, customer_support=data.customer_support,
        documentation_quality=data.documentation_quality, flexibility=data.flexibility,
        communication_effectiveness=data.communication_effectiveness, issue_resolution=data.issue_resolution,
        overall_rating=round(overall, 2), comments=data.comments
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_service_ratings(db: Session, vendor_id: int):
    return db.query(ServiceRating).filter(ServiceRating.vendor_id == vendor_id).all()
