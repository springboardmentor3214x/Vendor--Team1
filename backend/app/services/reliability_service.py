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

def get_reliability_dashboard(db: Session) -> Dict[str, Any]:
    all_vendors = db.query(Vendor).filter(Vendor.approval_status == "Approved").all()
    total_evaluated = len(all_vendors)

    if total_evaluated == 0:
        return {
            "total_vendors_evaluated": 0,
            "average_reliability_score": 0.0,
            "high_reliability_count": 0,
            "medium_reliability_count": 0,
            "high_risk_count": 0,
            "top_ranked_vendors": [],
            "risk_distribution": {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}
        }

    vendor_details = []
    for v in all_vendors:
        details = get_vendor_reliability_details(db, v.id)
        vendor_details.append(details)

    rated = [v for v in vendor_details if v["evaluated"]]
    high_rel = sum(1 for v in vendor_details if v["procurement_risk_level"] == "Low Risk")
    med_rel = sum(1 for v in vendor_details if v["procurement_risk_level"] == "Medium Risk")
    high_risk = sum(1 for v in vendor_details if v["procurement_risk_level"] == "High Risk")
    not_rated = sum(1 for v in vendor_details if v["procurement_risk_level"] == NOT_RATED)

    avg_score = round(sum(v["reliability_score"] for v in rated) / len(rated), 2) if rated else 0.0

    vendor_details.sort(key=lambda x: x["reliability_score"], reverse=True)
    top_ranked = [v for v in vendor_details if v["evaluated"]][:5]

    return {
        "total_vendors_evaluated": len(rated),
        "total_approved_vendors": total_evaluated,
        "average_reliability_score": avg_score,
        "high_reliability_count": high_rel,
        "medium_reliability_count": med_rel,
        "high_risk_count": high_risk,
        "not_rated_count": not_rated,
        "top_ranked_vendors": [
            {
                "vendor_id": v["vendor_id"],
                "vendor_name": v["vendor_name"],
                "company_name": v["company_name"],
                "category": v["category"],
                "reliability_score": v["reliability_score"],
                "risk_level": v["procurement_risk_level"],
                "recommendation_status": v["recommendation_status"]
            }
            for v in top_ranked
        ],
        "risk_distribution": {
            "Low Risk": high_rel,
            "Medium Risk": med_rel,
            "High Risk": high_risk,
            NOT_RATED: not_rated
        }
    }

def get_supplier_rankings(db: Session, category: Optional[str] = None) -> List[Dict[str, Any]]:
    query = db.query(Vendor).filter(Vendor.approval_status == "Approved")
    if category and category != "All":
        query = query.filter(Vendor.category == category)

    vendors = query.all()
    rankings = []

    for v in vendors:
        details = get_vendor_reliability_details(db, v.id)
        rankings.append({
            "vendor_id": v.id,
            "vendor_name": v.vendor_name,
            "company_name": v.company_name,
            "category": v.category,
            "reliability_score": details["reliability_score"],
            "procurement_risk_level": details["procurement_risk_level"],
            "recommendation_status": details["recommendation_status"],
            "delivery_score": details["reliability_factors"]["delivery_history"]["score"],
            "quality_score": details["reliability_factors"]["product_quality"]["score"],
            "communication_score": details["reliability_factors"]["communication_efficiency"]["score"],
            "service_score": details["reliability_factors"]["service_ratings"]["score"]
        })

    rankings.sort(key=lambda x: x["reliability_score"], reverse=True)
    for index, item in enumerate(rankings):
        item["vendor_rank"] = index + 1

    return rankings

def get_procurement_risk_assessment(db: Session) -> Dict[str, Any]:
    vendors = db.query(Vendor).filter(Vendor.approval_status == "Approved").all()
    low_risk, med_risk, high_risk, not_rated = [], [], [], []

    for v in vendors:
        details = get_vendor_reliability_details(db, v.id)
        item = {
            "vendor_id": v.id,
            "vendor_name": v.vendor_name,
            "company_name": v.company_name,
            "category": v.category,
            "reliability_score": details["reliability_score"],
            "risk_level": details["procurement_risk_level"],
            "warning_message": details["warning_message"]
        }
        level = details["procurement_risk_level"]
        if level == "Low Risk":
            low_risk.append(item)
        elif level == "Medium Risk":
            med_risk.append(item)
        elif level == NOT_RATED:
            not_rated.append(item)
        else:
            high_risk.append(item)

    return {
        "total_vendors": len(vendors),
        "low_risk_count": len(low_risk),
        "medium_risk_count": len(med_risk),
        "high_risk_count": len(high_risk),
        "not_rated_count": len(not_rated),
        "low_risk_vendors": low_risk,
        "medium_risk_vendors": med_risk,
        "high_risk_vendors": high_risk,
        "not_rated_vendors": not_rated,
        "high_risk_approval_required": True
    }

def _month_key(value) -> Optional[str]:
    return value.strftime("%Y-%m") if value else None


def _pending_reliability_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
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
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
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
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
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
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
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
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
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
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows
