from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict, Any
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.purchase_order import PurchaseOrder
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.services.performance_service import calculate_vendor_metrics, get_delivery_records, get_quality_records, get_communication_records, get_service_ratings
from app.core.risk import (
    calculate_risk_level,
    vendor_has_performance_data,
    LOW_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    NOT_RATED,
)

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

def calculate_recommendation_status(reliability_score: float, risk_level: str) -> str:
    if risk_level == "Low Risk":
        return "Highly Recommended"
    elif risk_level == "Medium Risk":
        return "Recommended with Caution"
    elif risk_level == NOT_RATED:
        return "Not Yet Evaluated"
    else:
        return "Not Recommended"

def get_contract_compliance_factor(db: Session, vendor_id: int) -> Dict[str, Any]:
    from app.models.compliance_record import ComplianceRecord
    from app.models.contract import Contract

    records = db.query(ComplianceRecord).filter(ComplianceRecord.vendor_id == vendor_id).all()
    total_contracts = db.query(Contract).filter(Contract.vendor_id == vendor_id).count()
    active_contracts = db.query(Contract).filter(
        Contract.vendor_id == vendor_id, Contract.status == "Active"
    ).count()

    if not records:
        return {
            "score": None,
            "total_checks": 0,
            "compliant_checks": 0,
            "compliance_rate": None,
            "total_contracts": total_contracts,
            "active_contracts": active_contracts,
        }

    compliant = sum(1 for r in records if (r.status or "").lower() == "compliant")
    rate = round(compliant / len(records) * 100, 2)
    return {
        "score": rate,
        "total_checks": len(records),
        "compliant_checks": compliant,
        "compliance_rate": rate,
        "total_contracts": total_contracts,
        "active_contracts": active_contracts,
    }

def get_vendor_reliability_details(db: Session, vendor_id: int) -> Dict[str, Any]:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        return None

    metrics = calculate_vendor_metrics(db, vendor_id)
    score = metrics["overall_performance_score"]
    has_data = vendor_has_performance_data(db, vendor_id)
    risk_level = calculate_risk_level(score, has_data)
    rec_status = calculate_recommendation_status(score, risk_level)

    factors = {
        "delivery_history": {
            "score": metrics["delivery_score"],
            "on_time_rate": metrics["on_time_rate"],
            "avg_delay_days": metrics["avg_delay_days"],
            "consistency_score": metrics["delivery_consistency"]
        },
        "product_quality": {
            "score": metrics["quality_score"],
            "avg_rating": metrics["avg_quality_rating"],
            "defect_rate": metrics["defect_rate"]
        },
        "communication_efficiency": {
            "score": metrics["communication_score"],
            "response_rate": metrics["response_rate"],
            "avg_response_hours": metrics["avg_response_hours"]
        },
        "service_ratings": {
            "score": metrics["service_score"],
            "avg_rating": metrics["avg_service_rating"]
        },
        "purchase_history": {
            "total_orders": metrics["total_orders"],
            "completed_orders": metrics["completed_orders"],
            "fulfillment_rate": metrics["fulfillment_rate"]
        },
        "contract_compliance": get_contract_compliance_factor(db, vendor_id),
        "issue_resolution": {
            "score": metrics["avg_issue_resolution"],
            "avg_rating": metrics["avg_issue_resolution"]
        }
    }

    warning_message = None
    if risk_level == "High Risk":
        warning_message = "WARNING: Assigning a Purchase Order to this High-Risk vendor requires special approval from Procurement Manager/Administrator."
    elif risk_level == NOT_RATED:
        warning_message = "This vendor has no performance history yet, so no reliability rating is available."

    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.vendor_name,
        "company_name": vendor.company_name,
        "category": vendor.category,
        "reliability_score": score,
        "evaluated": has_data,
        "procurement_risk_level": risk_level,
        "recommendation_status": rec_status,
        "warning_message": warning_message,
        "reliability_factors": factors,
        "full_metrics": metrics
    }


def _pending_reliability_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_reliability_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_reliability_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_reliability_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_reliability_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_reliability_service_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_reliability_service_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
