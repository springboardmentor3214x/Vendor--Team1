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

from app.models.vendor import Vendor

# ===== Performance Metrics =====
def calculate_vendor_metrics(db: Session, vendor_id: int):
    total_del = db.query(DeliveryPerformance).filter(DeliveryPerformance.vendor_id == vendor_id).count()
    on_time = db.query(DeliveryPerformance).filter(DeliveryPerformance.vendor_id == vendor_id, DeliveryPerformance.delivery_status.in_(["On-Time Delivery", "Early Delivery"])).count()
    delayed = db.query(DeliveryPerformance).filter(DeliveryPerformance.vendor_id == vendor_id, DeliveryPerformance.delivery_status == "Delayed Delivery").count()
    on_time_rate = round((on_time / total_del * 100), 2) if total_del > 0 else 0
    avg_quality = db.query(func.avg(QualityEvaluation.overall_rating)).filter(QualityEvaluation.vendor_id == vendor_id).scalar() or 0
    avg_response = db.query(func.avg(CommunicationLog.response_duration_hours)).filter(CommunicationLog.vendor_id == vendor_id, CommunicationLog.response_duration_hours.isnot(None)).scalar() or 0
    avg_service = db.query(func.avg(ServiceRating.overall_rating)).filter(ServiceRating.vendor_id == vendor_id).scalar() or 0

    delivery_score = on_time_rate
    quality_score = round(float(avg_quality) / 5.0 * 100, 2) if avg_quality else 0
    communication_score = max(0, round(100 - float(avg_response) * 5, 2)) if avg_response else 0
    service_score = round(float(avg_service) / 5.0 * 100, 2) if avg_service else 0
    overall = round(delivery_score * 0.3 + quality_score * 0.25 + communication_score * 0.2 + service_score * 0.25, 2)

    return {
        "vendor_id": vendor_id, "total_deliveries": total_del, "on_time_deliveries": on_time,
        "delayed_deliveries": delayed, "on_time_rate": on_time_rate,
        "avg_quality_rating": round(float(avg_quality), 2), "avg_response_hours": round(float(avg_response), 2),
        "avg_service_rating": round(float(avg_service), 2),
        "delivery_score": delivery_score, "quality_score": quality_score,
        "communication_score": communication_score, "service_score": service_score,
        "overall_performance_score": overall
    }


# ===== Vendor Ranking =====
def generate_vendor_rankings(db: Session):
    vendors = db.query(Vendor).all()
    rankings = []
    for v in vendors:
        m = calculate_vendor_metrics(db, v.id)
        rankings.append({
            "vendor_id": v.id, "vendor_name": v.vendor_name, "category": v.category,
            "overall_score": m["overall_performance_score"], "delivery_score": m["delivery_score"],
            "quality_score": m["quality_score"], "communication_score": m["communication_score"],
            "service_score": m["service_score"]
        })
    rankings.sort(key=lambda x: x["overall_score"], reverse=True)
    for i, r in enumerate(rankings):
        r["rank"] = i + 1
    return rankings

# ===== Performance Dashboard =====
def performance_dashboard(db: Session):
    total_vendors = db.query(Vendor).count()
    total_del = db.query(DeliveryPerformance).count()
    on_time = db.query(DeliveryPerformance).filter(DeliveryPerformance.delivery_status.in_(["On-Time Delivery", "Early Delivery"])).count()
    delayed = db.query(DeliveryPerformance).filter(DeliveryPerformance.delivery_status == "Delayed Delivery").count()
    avg_quality = db.query(func.avg(QualityEvaluation.overall_rating)).scalar() or 0
    avg_response = db.query(func.avg(CommunicationLog.response_duration_hours)).filter(CommunicationLog.response_duration_hours.isnot(None)).scalar() or 0
    return {
        "total_vendors_evaluated": total_vendors, "total_deliveries": total_del,
        "on_time_deliveries": on_time, "delayed_deliveries": delayed,
        "avg_delivery_performance": round((on_time / total_del * 100), 2) if total_del > 0 else 0,
        "avg_quality_rating": round(float(avg_quality), 2),
        "avg_response_time_hours": round(float(avg_response), 2)
    }


# ===== Performance History =====
def get_vendor_performance_history(db: Session, vendor_id: int):
    deliveries = get_delivery_records(db, vendor_id)
    quality = get_quality_records(db, vendor_id)
    communications = get_communication_records(db, vendor_id)
    ratings = get_service_ratings(db, vendor_id)
    metrics = calculate_vendor_metrics(db, vendor_id)
    return {
        "vendor_id": vendor_id,
        "delivery_records": [{"id": d.id, "status": d.delivery_status, "delay_days": d.delay_days} for d in deliveries],
        "quality_evaluations": [{"id": q.id, "overall_rating": q.overall_rating} for q in quality],
        "communication_logs": [{"id": c.id, "response_hours": c.response_duration_hours, "status": c.communication_status} for c in communications],
        "service_ratings": [{"id": s.id, "overall_rating": s.overall_rating} for s in ratings],
        "current_metrics": metrics
    }
