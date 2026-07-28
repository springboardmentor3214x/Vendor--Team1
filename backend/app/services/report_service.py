from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import os
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as RLTable, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.purchase_order import PurchaseOrder
from app.models.invoice import Invoice
from app.models.contract import Contract
from app.models.compliance_record import ComplianceRecord
from app.models.certification import Certification
from app.models.user import User
from app.models.order_tracking import OrderTracking
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating

RUPEE = "₹"

def _as_datetime(value, end_of_day: bool = False):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.max.time() if end_of_day else datetime.min.time())
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.replace(tzinfo=None)
    except ValueError:
        return None

def _apply_date_range(query, column, start_date, end_date):
    start = _as_datetime(start_date)
    end = _as_datetime(end_date, end_of_day=True)
    if start is not None:
        query = query.filter(column >= start)
    if end is not None:
        query = query.filter(column <= end)
    return query

def format_currency(amount: Optional[float]) -> str:
    return f"{RUPEE}{float(amount or 0.0):,.2f}"

def describe_filters(**filters) -> str:
    applied = [f"{k.replace('_', ' ').title()}: {v}" for k, v in filters.items() if v not in (None, "", "All")]
    return " | ".join(applied) if applied else "None"

def get_vendor_performance_report(
    db: Session,
    category: Optional[str] = None,
    min_reliability: Optional[float] = None,
    start_date=None,
    end_date=None
) -> List[Dict[str, Any]]:
    query = db.query(Vendor)
    if category and category != "All":
        query = query.filter(Vendor.category == category)
    if min_reliability is not None:
        query = query.filter(Vendor.reliability_score >= min_reliability)

    vendors = query.all()
    results = []
    for v in vendors:
        po_query = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == v.id)
        po_query = _apply_date_range(po_query, PurchaseOrder.po_date, start_date, end_date)
        vendor_pos = po_query.all()
        total_pos = len(vendor_pos)
        completed_pos = sum(1 for po in vendor_pos if po.status in ("Delivered", "Completed"))

        delivery_query = db.query(DeliveryPerformance).filter(DeliveryPerformance.vendor_id == v.id)
        delivery_query = _apply_date_range(delivery_query, DeliveryPerformance.actual_date, start_date, end_date)
        deliveries = delivery_query.all()
        on_time = sum(1 for d in deliveries if (d.delay_days or 0) <= 0)
        delayed = sum(1 for d in deliveries if (d.delay_days or 0) > 0)
        on_time_rate = round(on_time / len(deliveries) * 100, 2) if deliveries else 0.0

        quality_query = db.query(QualityEvaluation).filter(QualityEvaluation.vendor_id == v.id)
        quality_query = _apply_date_range(quality_query, QualityEvaluation.inspection_date, start_date, end_date)
        quality_rows = quality_query.all()
        avg_quality = round(sum(q.overall_rating or 0 for q in quality_rows) / len(quality_rows), 2) if quality_rows else 0.0

        comm_query = db.query(CommunicationLog).filter(CommunicationLog.vendor_id == v.id)
        comm_query = _apply_date_range(comm_query, CommunicationLog.message_sent_time, start_date, end_date)
        comm_rows = [c for c in comm_query.all() if c.response_duration_hours is not None]
        avg_response_hours = round(sum(c.response_duration_hours for c in comm_rows) / len(comm_rows), 2) if comm_rows else 0.0

        service_query = db.query(ServiceRating).filter(ServiceRating.vendor_id == v.id)
        service_query = _apply_date_range(service_query, ServiceRating.rated_at, start_date, end_date)
        service_rows = service_query.all()
        avg_service = round(sum(s.overall_rating or 0 for s in service_rows) / len(service_rows), 2) if service_rows else 0.0

        results.append({
            "on_time_delivery_rate": on_time_rate,
            "delayed_deliveries": delayed,
            "avg_quality_rating": avg_quality,
            "avg_response_hours": avg_response_hours,
            "avg_service_rating": avg_service,
            "vendor_id": v.id,
            "vendor_name": v.vendor_name,
            "company_name": v.company_name,
            "category": v.category or "General",
            "approval_status": v.approval_status,
            "reliability_score": round(v.reliability_score or 0.0, 2),
            "delivery_score": round(v.delivery_score or 0.0, 2),
            "quality_score": round(v.quality_score or 0.0, 2),
            "communication_score": round(v.communication_score or 0.0, 2),
            "service_score": round(v.service_score or 0.0, 2),
            "total_pos": total_pos,
            "completed_pos": completed_pos
        })
    return results

def get_procurement_report(
    db: Session,
    department: Optional[str] = None,
    status: Optional[str] = None,
    start_date=None,
    end_date=None
) -> Dict[str, Any]:
    query = db.query(Procurement)
    if department and department != "All":
        query = query.filter(Procurement.department == department)
    if status and status != "All":
        query = query.filter(Procurement.status == status)
    query = _apply_date_range(query, Procurement.created_at, start_date, end_date)

    requests = query.all()
    total_count = len(requests)
    pending_count = sum(1 for r in requests if r.approval_status == "Pending")
    approved_count = sum(1 for r in requests if r.approval_status == "Approved")
    rejected_count = sum(1 for r in requests if r.approval_status == "Rejected")
    completed_count = sum(1 for r in requests if r.status == "Completed")

    procurement_ids = [r.id for r in requests]
    pos_generated = (
        db.query(PurchaseOrder).filter(PurchaseOrder.procurement_id.in_(procurement_ids)).count()
        if procurement_ids else 0
    )

    total_expenditure = sum(r.total_price or 0.0 for r in requests)

    departments: Dict[str, Dict[str, Any]] = {}
    for r in requests:
        key = r.department or "Unassigned"
        bucket = departments.setdefault(key, {"department": key, "request_count": 0, "total_spend": 0.0})
        bucket["request_count"] += 1
        bucket["total_spend"] += float(r.total_price or 0.0)

    items = [
        {
            "id": r.id,
            "title": r.request_title or r.item_name,
            "department": r.department,
            "category": r.category,
            "quantity": r.quantity,
            "total_price": float(r.total_price or 0.0),
            "approval_status": r.approval_status,
            "status": r.status,
            "created_at": r.created_at.strftime("%Y-%m-%d") if r.created_at else ""
        }
        for r in requests
    ]

    return {
        "summary": {
            "total_requests": total_count,
            "pending_approvals": pending_count,
            "approved_requests": approved_count,
            "rejected_requests": rejected_count,
            "completed_requests": completed_count,
            "purchase_orders_generated": pos_generated,
            "total_expenditure": float(total_expenditure)
        },
        "department_breakdown": sorted(departments.values(), key=lambda d: d["total_spend"], reverse=True),
        "items": items
    }

def get_po_report(
    db: Session,
    status: Optional[str] = None,
    vendor_id: Optional[int] = None,
    start_date=None,
    end_date=None
) -> List[Dict[str, Any]]:
    query = db.query(PurchaseOrder)
    if status and status != "All":
        query = query.filter(PurchaseOrder.status == status)
    if vendor_id:
        query = query.filter(PurchaseOrder.vendor_id == vendor_id)
    query = _apply_date_range(query, PurchaseOrder.po_date, start_date, end_date)

    orders = query.all()
    results = []
    for po in orders:
        invoice = db.query(Invoice).filter(Invoice.po_id == po.id).first()
        tracking = db.query(OrderTracking).filter(OrderTracking.po_id == po.id).first()
        results.append({
            "po_id": po.id,
            "po_number": po.po_number,
            "vendor_name": po.vendor_name,
            "item_name": po.item_name,
            "total_cost": float(po.total_cost or 0.0),
            "tax_amount": float(po.tax_amount or 0.0),
            "status": po.status,
            "invoice_status": invoice.payment_status if invoice else "Not Raised",
            "issued_date": po.po_date.strftime("%Y-%m-%d") if po.po_date else "",
            "expected_delivery_date": po.expected_delivery_date.strftime("%Y-%m-%d") if po.expected_delivery_date else "",
            "actual_delivery_date": (
                tracking.actual_delivery_date.strftime("%Y-%m-%d")
                if tracking and tracking.actual_delivery_date else ""
            )
        })
    return results

def get_compliance_report(db: Session, status: Optional[str] = None, start_date=None, end_date=None) -> Dict[str, Any]:
    query = db.query(ComplianceRecord)
    if status and status != "All":
        query = query.filter(ComplianceRecord.status == status)
    query = _apply_date_range(query, ComplianceRecord.created_at, start_date, end_date)

    records = query.all()
    total_records = len(records)
    compliant_count = sum(1 for r in records if r.status == "Compliant")
    pending_count = sum(1 for r in records if r.status == "Pending Verification")
    non_compliant_count = sum(1 for r in records if r.status in ("Non-Compliant", "Expired"))

    vendor_names = {v.id: (v.company_name or v.vendor_name) for v in db.query(Vendor).all()}

    items = [
        {
            "id": r.id,
            "vendor_id": r.vendor_id,
            "vendor_name": vendor_names.get(r.vendor_id, f"Vendor #{r.vendor_id}"),
            "compliance_type": r.compliance_type,
            "status": r.status,
            "verified_by": r.verified_by,
            "verification_date": r.verification_date.strftime("%Y-%m-%d") if r.verification_date else "",
            "expiry_date": r.expiry_date.strftime("%Y-%m-%d") if r.expiry_date else ""
        }
        for r in records
    ]

    today = date.today()
    cert_query = db.query(Certification)
    cert_query = _apply_date_range(cert_query, Certification.created_at, start_date, end_date)
    certifications = cert_query.all()
    expired_certs = [c for c in certifications if c.expiry_date and c.expiry_date < today]
    expiring_certs = [c for c in certifications if c.expiry_date and today <= c.expiry_date <= today + timedelta(days=30)]

    approved_vendor_ids = {
        v.id for v in db.query(Vendor).filter(Vendor.approval_status == "Approved").all()
    }
    vendors_with_records = {r.vendor_id for r in records}
    missing_documents = [
        {"vendor_id": vid, "vendor_name": vendor_names.get(vid, f"Vendor #{vid}")}
        for vid in sorted(approved_vendor_ids - vendors_with_records)
    ]

    return {
        "summary": {
            "total_records": total_records,
            "compliant_count": compliant_count,
            "pending_count": pending_count,
            "non_compliant_count": non_compliant_count,
            "total_certifications": len(certifications),
            "expired_certifications": len(expired_certs),
            "expiring_certifications": len(expiring_certs),
            "missing_document_vendors": len(missing_documents),
            "compliance_rate": round((compliant_count / total_records * 100), 2) if total_records > 0 else 100.0
        },
        "items": items,
        "certifications": [
            {
                "id": c.id,
                "vendor_id": c.vendor_id,
                "vendor_name": vendor_names.get(c.vendor_id, f"Vendor #{c.vendor_id}"),
                "certification_name": c.certification_name,
                "certificate_number": c.certificate_number,
                "issuing_authority": c.issuing_authority,
                "issue_date": c.issue_date.strftime("%Y-%m-%d") if c.issue_date else "",
                "expiry_date": c.expiry_date.strftime("%Y-%m-%d") if c.expiry_date else "",
                "status": "Expired" if c.expiry_date and c.expiry_date < today else c.status
            }
            for c in certifications
        ],
        "missing_documents": missing_documents
    }

def get_contract_report(db: Session, status: Optional[str] = None, start_date=None, end_date=None,
                        expiring_within_days: Optional[int] = None) -> List[Dict[str, Any]]:
    query = db.query(Contract)
    if status and status != "All":
        query = query.filter(Contract.status == status)
    query = _apply_date_range(query, Contract.created_at, start_date, end_date)

    contracts = query.all()
    today = date.today()

    if expiring_within_days is not None:
        cutoff = today + timedelta(days=expiring_within_days)
        contracts = [c for c in contracts if c.end_date and today <= c.end_date <= cutoff]

    return [
        {
            "id": c.id,
            "contract_number": c.contract_number,
            "contract_title": c.contract_title,
            "vendor_name": c.vendor_name,
            "contract_type": c.contract_type,
            "contract_value": float(c.contract_value or 0.0),
            "payment_terms": c.payment_terms,
            "responsible_manager": c.responsible_manager,
            "status": c.status,
            "days_to_expiry": (c.end_date - today).days if c.end_date else None,
            "start_date": c.start_date.strftime("%Y-%m-%d") if c.start_date else "",
            "end_date": c.end_date.strftime("%Y-%m-%d") if c.end_date else ""
        }
        for c in contracts
    ]

def get_executive_summary_report(db: Session, start_date=None, end_date=None) -> Dict[str, Any]:
    today = date.today()

    total_vendors = db.query(Vendor).count()
    approved_vendors = db.query(Vendor).filter(Vendor.approval_status == "Approved").count()
    active_vendors = db.query(Vendor).filter(Vendor.status == "Active").count()

    proc_query = _apply_date_range(db.query(Procurement), Procurement.created_at, start_date, end_date)
    procurements = proc_query.all()
    total_proc = len(procurements)
    total_expenditure = sum(p.total_price or 0.0 for p in procurements)
    completed_proc = sum(1 for p in procurements if p.status == "Completed")

    po_query = _apply_date_range(db.query(PurchaseOrder), PurchaseOrder.po_date, start_date, end_date)
    purchase_orders = po_query.all()
    total_pos = len(purchase_orders)
    completed_pos = sum(1 for po in purchase_orders if po.status in ("Delivered", "Completed"))

    total_contracts = db.query(Contract).count()
    active_contracts = db.query(Contract).filter(Contract.status == "Active").count()
    near_expiry = db.query(Contract).filter(
        Contract.end_date >= today,
        Contract.end_date <= today + timedelta(days=60)
    ).count()

    comp_records = db.query(ComplianceRecord).count()
    compliant_count = db.query(ComplianceRecord).filter(ComplianceRecord.status == "Compliant").count()

    delivery_query = _apply_date_range(
        db.query(DeliveryPerformance), DeliveryPerformance.actual_date, start_date, end_date
    )
    deliveries = delivery_query.all()
    delayed_deliveries = sum(1 for d in deliveries if (d.delay_days or 0) > 0)

    from app.core.risk import calculate_risk_level
    distribution = {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}
    for v in db.query(Vendor).filter(Vendor.approval_status == "Approved").all():
        distribution[calculate_risk_level(v.reliability_score)] += 1

    top_vendors = [
        {
            "vendor_id": v.id,
            "company_name": v.company_name,
            "category": v.category,
            "reliability_score": round(v.reliability_score or 0.0, 2)
        }
        for v in db.query(Vendor)
        .filter(Vendor.approval_status == "Approved")
        .order_by(Vendor.reliability_score.desc())
        .limit(5)
        .all()
    ]

    monthly: Dict[str, float] = {}
    for p in procurements:
        if not p.created_at:
            continue
        key = p.created_at.strftime("%Y-%m")
        monthly[key] = monthly.get(key, 0.0) + float(p.total_price or 0.0)
    monthly_trends = [{"period": k, "total_spend": round(v, 2)} for k, v in sorted(monthly.items())]

    return {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "vendor_overview": {
            "total_vendors": total_vendors,
            "approved_vendors": approved_vendors,
            "active_vendors": active_vendors,
            "reliability_distribution": distribution,
            "top_vendors": top_vendors
        },
        "procurement_overview": {
            "total_requests": total_proc,
            "completed_requests": completed_proc,
            "total_expenditure": float(total_expenditure),
            "total_purchase_orders": total_pos,
            "delayed_deliveries": delayed_deliveries,
            "po_completion_rate": round((completed_pos / total_pos * 100), 2) if total_pos > 0 else 0.0
        },
        "contract_overview": {
            "total_contracts": total_contracts,
            "active_contracts": active_contracts,
            "contracts_near_expiry": near_expiry
        },
        "compliance_overview": {
            "total_records": comp_records,
            "compliance_percentage": round((compliant_count / comp_records * 100), 2) if comp_records > 0 else 100.0
        },
        "monthly_trends": monthly_trends
    }


def _pending_report_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_report_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_report_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_report_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_report_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_report_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_report_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_report_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_report_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_report_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
