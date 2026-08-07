from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.models.vendor import Vendor
from app.schemas.performance import (
    DeliveryPerformanceCreate, QualityEvaluationCreate,
    CommunicationLogCreate, ServiceRatingCreate
)
from app.utils.delivery_timing import delivery_status_from_times


def record_delivery(db: Session, data: DeliveryPerformanceCreate):
    status, delay_hours, delay_days = delivery_status_from_times(
        data.expected_date, data.actual_date
    )

    record = DeliveryPerformance(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        expected_date=data.expected_date, actual_date=data.actual_date,
        delay_days=delay_days, delay_hours=delay_hours,
        delivery_status=status, remarks=data.remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_delivery_records(db: Session, vendor_id: int):
    return db.query(DeliveryPerformance).filter(
        DeliveryPerformance.vendor_id == vendor_id
    ).all()


def record_quality(db: Session, data: QualityEvaluationCreate):
    overall = (
        data.material_quality + data.packaging_quality +
        data.quantity_accuracy + data.specification_compliance
    ) / 4.0

    record = QualityEvaluation(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        material_quality=data.material_quality,
        packaging_quality=data.packaging_quality,
        quantity_accuracy=data.quantity_accuracy,
        specification_compliance=data.specification_compliance,
        defect_count=data.defect_count,
        overall_rating=round(overall, 2), remarks=data.remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_quality_records(db: Session, vendor_id: int):
    return db.query(QualityEvaluation).filter(
        QualityEvaluation.vendor_id == vendor_id
    ).all()


def record_communication(db: Session, data: CommunicationLogCreate):
    duration = None
    comm_status = "Pending"

    if data.vendor_response_time:
        delta = data.vendor_response_time - data.message_sent_time
        duration = round(delta.total_seconds() / 3600, 2)
        comm_status = "Responded"

    record = CommunicationLog(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        message_sent_time=data.message_sent_time,
        vendor_response_time=data.vendor_response_time,
        response_duration_hours=duration,
        communication_status=comm_status, remarks=data.remarks
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_communication_records(db: Session, vendor_id: int):
    return db.query(CommunicationLog).filter(
        CommunicationLog.vendor_id == vendor_id
    ).all()


def submit_service_rating(db: Session, data: ServiceRatingCreate):
    overall = (
        data.professionalism + data.customer_support +
        data.documentation_quality + data.flexibility +
        data.communication_effectiveness + data.issue_resolution
    ) / 6.0

    record = ServiceRating(
        procurement_id=data.procurement_id, vendor_id=data.vendor_id,
        professionalism=data.professionalism,
        customer_support=data.customer_support,
        documentation_quality=data.documentation_quality,
        flexibility=data.flexibility,
        communication_effectiveness=data.communication_effectiveness,
        issue_resolution=data.issue_resolution,
        overall_rating=round(overall, 2), comments=data.comments
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_service_ratings(db: Session, vendor_id: int):
    return db.query(ServiceRating).filter(
        ServiceRating.vendor_id == vendor_id
    ).all()


def calculate_vendor_metrics(db: Session, vendor_id: int):
    deliveries = db.query(DeliveryPerformance).filter(
        DeliveryPerformance.vendor_id == vendor_id
    ).all()
    total_del = len(deliveries)

    if total_del > 0:
        on_time = sum(
            1 for d in deliveries
            if d.delivery_status in ("Delivered On Time", "Delivered Early")
        )
        early = sum(1 for d in deliveries if d.delivery_status == "Delivered Early")
        delayed = total_del - on_time

        on_time_rate = round(on_time / total_del * 100, 2)
        early_delivery_bonus = round(early / total_del * 10, 2)

        delay_hours_list = [
            d.delay_hours for d in deliveries
            if d.delay_hours is not None and d.delay_hours > 0
        ]
        avg_delay_hours = round(
            sum(delay_hours_list) / len(delay_hours_list), 2
        ) if delay_hours_list else 0
        avg_delay = avg_delay_hours / 24
        delay_penalty = min(avg_delay_hours * 0.8, 30)

        all_delays = [d.delay_days or 0 for d in deliveries]
        mean_delay = sum(all_delays) / len(all_delays)
        variance = sum((x - mean_delay) ** 2 for x in all_delays) / len(all_delays)
        std_dev = variance ** 0.5
        consistency_score = max(0, round(100 - std_dev * 10, 2))

        delivery_score = min(100, max(0, round(
            on_time_rate * 0.50 +
            early_delivery_bonus +
            consistency_score * 0.30 -
            delay_penalty
        , 2)))
    else:
        on_time = early = delayed = 0
        on_time_rate = avg_delay = 0
        consistency_score = 0
        delivery_score = 0

    quality_evals = db.query(QualityEvaluation).filter(
        QualityEvaluation.vendor_id == vendor_id
    ).all()

    if quality_evals:
        avg_material = sum(q.material_quality for q in quality_evals) / len(quality_evals)
        avg_packaging = sum(q.packaging_quality for q in quality_evals) / len(quality_evals)
        avg_spec_compliance = sum(q.specification_compliance for q in quality_evals) / len(quality_evals)
        avg_qty_accuracy = sum(q.quantity_accuracy for q in quality_evals) / len(quality_evals)
        avg_quality_overall = sum(q.overall_rating for q in quality_evals) / len(quality_evals)
        total_defects = sum(q.defect_count or 0 for q in quality_evals)
        total_items_evaluated = len(quality_evals)
        defect_rate = total_defects / total_items_evaluated if total_items_evaluated > 0 else 0
        defect_penalty = min(defect_rate * 5, 20)

        quality_score = min(100, max(0, round(
            (avg_material / 5 * 100) * 0.25 +
            (avg_packaging / 5 * 100) * 0.15 +
            (avg_spec_compliance / 5 * 100) * 0.25 +
            (avg_qty_accuracy / 5 * 100) * 0.20 +
            (avg_quality_overall / 5 * 100) * 0.15 -
            defect_penalty
        , 2)))
    else:
        avg_material = avg_packaging = avg_spec_compliance = avg_qty_accuracy = 0
        avg_quality_overall = 0
        defect_rate = 0
        quality_score = 0

    comm_logs = db.query(CommunicationLog).filter(
        CommunicationLog.vendor_id == vendor_id
    ).all()

    if comm_logs:
        total_messages = len(comm_logs)
        responded = [c for c in comm_logs if c.communication_status == "Responded"]
        response_rate = round(len(responded) / total_messages * 100, 2)

        response_scores = []
        for c in responded:
            hours = c.response_duration_hours or 0
            if hours <= 2:
                response_scores.append(100)
            elif hours <= 6:
                response_scores.append(80)
            elif hours <= 12:
                response_scores.append(60)
            elif hours <= 24:
                response_scores.append(40)
            else:
                response_scores.append(20)

        avg_response_time_score = round(sum(response_scores) / len(response_scores), 2) if response_scores else 0
        avg_response_hours = round(
            sum(c.response_duration_hours or 0 for c in responded) / len(responded), 2
        ) if responded else 0

        communication_score = min(100, max(0, round(
            avg_response_time_score * 0.50 +
            response_rate * 0.35 +
            min(len(responded), 10) * 1.5
        , 2)))
    else:
        total_messages = 0
        response_rate = 0
        avg_response_time_score = 0
        avg_response_hours = 0
        communication_score = 0

    service_ratings = db.query(ServiceRating).filter(
        ServiceRating.vendor_id == vendor_id
    ).all()

    if service_ratings:
        avg_professionalism = sum(s.professionalism for s in service_ratings) / len(service_ratings)
        avg_customer_support = sum(s.customer_support for s in service_ratings) / len(service_ratings)
        avg_documentation = sum(s.documentation_quality for s in service_ratings) / len(service_ratings)
        avg_flexibility = sum(s.flexibility for s in service_ratings) / len(service_ratings)
        avg_comm_effectiveness = sum(s.communication_effectiveness for s in service_ratings) / len(service_ratings)
        avg_issue_resolution = sum(s.issue_resolution for s in service_ratings) / len(service_ratings)
        avg_service_overall = sum(s.overall_rating for s in service_ratings) / len(service_ratings)

        service_score = min(100, max(0, round(
            (avg_professionalism / 5 * 100) * 0.20 +
            (avg_customer_support / 5 * 100) * 0.20 +
            (avg_issue_resolution / 5 * 100) * 0.20 +
            (avg_documentation / 5 * 100) * 0.15 +
            (avg_flexibility / 5 * 100) * 0.10 +
            (avg_comm_effectiveness / 5 * 100) * 0.15
        , 2)))
    else:
        avg_professionalism = avg_customer_support = avg_documentation = 0
        avg_flexibility = avg_comm_effectiveness = avg_issue_resolution = 0
        avg_service_overall = 0
        service_score = 0

    from app.models.procurement import Procurement
    total_orders = db.query(Procurement).filter(Procurement.vendor_id == vendor_id).count()
    completed_orders = db.query(Procurement).filter(
        Procurement.vendor_id == vendor_id,
        Procurement.status.in_(["Completed", "Delivered"])
    ).count()
    rejected_orders = db.query(Procurement).filter(
        Procurement.vendor_id == vendor_id,
        Procurement.status == "Rejected"
    ).count()

    if total_orders > 0:
        fulfillment_rate = round(completed_orders / total_orders * 100, 2)
        rejection_penalty = round(rejected_orders / total_orders * 20, 2)
        volume_bonus = min(total_orders * 2, 10)

        reliability_index = min(100, max(0, round(
            fulfillment_rate * 0.70 +
            volume_bonus -
            rejection_penalty +
            (on_time_rate * 0.20 if total_del > 0 else 0)
        , 2)))
    else:
        fulfillment_rate = 0
        rejection_penalty = 0
        volume_bonus = 0
        reliability_index = 0

    overall = round(
        delivery_score * 0.30 +
        quality_score * 0.25 +
        communication_score * 0.20 +
        service_score * 0.15 +
        reliability_index * 0.10
    , 2)

    return {
        "vendor_id": vendor_id,
        "total_deliveries": total_del,
        "on_time_deliveries": on_time if total_del > 0 else 0,
        "early_deliveries": early if total_del > 0 else 0,
        "delayed_deliveries": delayed if total_del > 0 else 0,
        "on_time_rate": on_time_rate if total_del > 0 else 0,
        "avg_delay_days": avg_delay if total_del > 0 else 0,
        "delivery_consistency": consistency_score if total_del > 0 else 0,
        "delivery_score": delivery_score,
        "avg_material_quality": round(float(avg_material), 2) if quality_evals else 0,
        "avg_packaging_quality": round(float(avg_packaging), 2) if quality_evals else 0,
        "avg_spec_compliance": round(float(avg_spec_compliance), 2) if quality_evals else 0,
        "avg_quantity_accuracy": round(float(avg_qty_accuracy), 2) if quality_evals else 0,
        "avg_quality_rating": round(float(avg_quality_overall), 2) if quality_evals else 0,
        "defect_rate": round(float(defect_rate), 2) if quality_evals else 0,
        "quality_score": quality_score,
        "total_messages": total_messages if comm_logs else 0,
        "response_rate": response_rate if comm_logs else 0,
        "avg_response_time_score": avg_response_time_score if comm_logs else 0,
        "avg_response_hours": avg_response_hours if comm_logs else 0,
        "communication_score": communication_score,
        "avg_professionalism": round(float(avg_professionalism), 2) if service_ratings else 0,
        "avg_customer_support": round(float(avg_customer_support), 2) if service_ratings else 0,
        "avg_documentation_quality": round(float(avg_documentation), 2) if service_ratings else 0,
        "avg_flexibility": round(float(avg_flexibility), 2) if service_ratings else 0,
        "avg_communication_effectiveness": round(float(avg_comm_effectiveness), 2) if service_ratings else 0,
        "avg_issue_resolution": round(float(avg_issue_resolution), 2) if service_ratings else 0,
        "avg_service_rating": round(float(avg_service_overall), 2) if service_ratings else 0,
        "service_score": service_score,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "fulfillment_rate": fulfillment_rate,
        "reliability_index": reliability_index,
        "overall_performance_score": overall
    }


def generate_vendor_rankings(db: Session):
    vendors = db.query(Vendor).all()
    rankings = []

    for v in vendors:
        m = calculate_vendor_metrics(db, v.id)
        rankings.append({
            "vendor_id": v.id,
            "vendor_name": v.vendor_name,
            "category": v.category,
            "overall_score": m["overall_performance_score"],
            "delivery_score": m["delivery_score"],
            "quality_score": m["quality_score"],
            "communication_score": m["communication_score"],
            "service_score": m["service_score"]
        })

    rankings.sort(key=lambda x: x["overall_score"], reverse=True)
    for i, r in enumerate(rankings):
        r["rank"] = i + 1

    return rankings


def performance_dashboard(db: Session):
    total_vendors = db.query(Vendor).count()
    total_del = db.query(DeliveryPerformance).count()
    on_time = db.query(DeliveryPerformance).filter(
        DeliveryPerformance.delivery_status.in_(["Delivered On Time", "Delivered Early"])
    ).count()
    delayed = db.query(DeliveryPerformance).filter(
        ~DeliveryPerformance.delivery_status.in_(["Delivered On Time", "Delivered Early"])
    ).count()
    avg_quality = db.query(func.avg(QualityEvaluation.overall_rating)).scalar() or 0
    avg_response = db.query(func.avg(CommunicationLog.response_duration_hours)).filter(
        CommunicationLog.response_duration_hours.isnot(None)
    ).scalar() or 0

    return {
        "total_vendors_evaluated": total_vendors,
        "total_deliveries": total_del,
        "on_time_deliveries": on_time,
        "delayed_deliveries": delayed,
        "avg_delivery_performance": round((on_time / total_del * 100), 2) if total_del > 0 else 0,
        "avg_quality_rating": round(float(avg_quality), 2),
        "avg_response_time_hours": round(float(avg_response), 2)
    }


def get_vendor_performance_history(db: Session, vendor_id: int):
    deliveries = get_delivery_records(db, vendor_id)
    quality = get_quality_records(db, vendor_id)
    communications = get_communication_records(db, vendor_id)
    ratings = get_service_ratings(db, vendor_id)
    metrics = calculate_vendor_metrics(db, vendor_id)

    return {
        "vendor_id": vendor_id,
        "delivery_records": [
            {"id": d.id, "status": d.delivery_status, "delay_days": d.delay_days}
            for d in deliveries
        ],
        "quality_evaluations": [
            {"id": q.id, "overall_rating": q.overall_rating}
            for q in quality
        ],
        "communication_logs": [
            {"id": c.id, "response_hours": c.response_duration_hours,
             "status": c.communication_status}
            for c in communications
        ],
        "service_ratings": [
            {"id": s.id, "overall_rating": s.overall_rating}
            for s in ratings
        ],
        "current_metrics": metrics
    }
