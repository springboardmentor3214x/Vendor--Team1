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


def _pending_report_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_report_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_report_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_report_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_report_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_report_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_report_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_report_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_report_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_report_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_report_service_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_report_service_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
