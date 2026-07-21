from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from app.models.user import User
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.purchase_order import PurchaseOrder
from app.models.contract import Contract
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication import Communication
from app.models.compliance_record import ComplianceRecord
from app.models.certification import Certification
from app.models.invoice import Invoice

ACTIVE_PO_STATUSES = ["Issued", "In Transit"]

COMPLETED_PO_STATUSES = ["Delivered", "Completed"]

def get_procurement_manager_dashboard_analytics(db: Session) -> Dict[str, Any]:
    total_requests = db.query(Procurement).count()
    pending_approvals = db.query(Procurement).filter(Procurement.approval_status == "Pending").count()
    active_pos = db.query(PurchaseOrder).filter(PurchaseOrder.status.in_(ACTIVE_PO_STATUSES)).count()
    completed_orders = db.query(Procurement).filter(Procurement.status == "Completed").count()
    cancelled_orders = db.query(Procurement).filter(Procurement.status == "Cancelled").count()

    total_cost_res = db.query(func.sum(Procurement.total_price)).scalar() or 0.0
    total_po_cost = db.query(func.sum(PurchaseOrder.total_cost)).scalar() or 0.0

    dept_spending = db.query(
        Procurement.department, func.sum(Procurement.total_price), func.count(Procurement.id)
    ).group_by(Procurement.department).all()

    department_breakdown = [
        {"department": dept or "General", "total_spending": float(spend or 0.0), "request_count": count}
        for dept, spend, count in dept_spending
    ]

    cat_spending = db.query(
        Procurement.category, func.sum(Procurement.total_price), func.count(Procurement.id)
    ).group_by(Procurement.category).all()

    category_breakdown = [
        {"category": cat or "General", "total_spending": float(spend or 0.0), "request_count": count}
        for cat, spend, count in cat_spending
    ]

    today = date.today()
    monthly_trends = []
    for i in range(5, -1, -1):
        target_month = (today.month - i - 1) % 12 + 1
        target_year = today.year if today.month - i > 0 else today.year - 1
        month_name = date(target_year, target_month, 1).strftime("%b %Y")

        val = db.query(func.sum(Procurement.total_price)).filter(
            extract('year', Procurement.created_at) == target_year,
            extract('month', Procurement.created_at) == target_month
        ).scalar() or 0.0

        count = db.query(func.count(Procurement.id)).filter(
            extract('year', Procurement.created_at) == target_year,
            extract('month', Procurement.created_at) == target_month
        ).scalar() or 0

        monthly_trends.append({
            "month": month_name,
            "total_spending": float(val),
            "request_count": count
        })

    active_po_list = db.query(PurchaseOrder).filter(PurchaseOrder.status.in_(["Issued", "In Transit"])).limit(10).all()
    po_summary = [
        {
            "po_id": po.id,
            "po_number": po.po_number,
            "vendor_name": po.vendor_name,
            "total_cost": po.total_cost,
            "status": po.status,
            "expected_delivery_date": po.expected_delivery_date,
            "is_delayed": bool(po.expected_delivery_date and po.expected_delivery_date < datetime.utcnow())
        }
        for po in active_po_list
    ]

    return {
        "summary": {
            "total_procurement_requests": total_requests,
            "pending_approvals": pending_approvals,
            "active_purchase_orders": active_pos,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            "total_expenditure": float(total_cost_res),
            "total_purchase_order_value": float(total_po_cost)
        },
        "procurement_overview": get_procurement_overview(db),
        "delivery_status": get_delivery_status_summary(db),
        "department_breakdown": department_breakdown,
        "category_breakdown": category_breakdown,
        "monthly_trends": monthly_trends,
        "active_purchase_orders_list": po_summary
    }

def get_procurement_overview(db: Session) -> Dict[str, Any]:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    def requests_since(start: date) -> int:
        return db.query(func.count(Procurement.id)).filter(
            func.date(Procurement.created_at) >= start
        ).scalar() or 0

    def spending_since(start: date) -> float:
        return float(db.query(func.sum(Procurement.total_price)).filter(
            func.date(Procurement.created_at) >= start
        ).scalar() or 0.0)

    completed_this_week = db.query(func.count(PurchaseOrder.id)).filter(
        PurchaseOrder.status.in_(COMPLETED_PO_STATUSES),
        func.date(PurchaseOrder.po_date) >= week_start
    ).scalar() or 0

    last_year_requests = db.query(func.count(Procurement.id)).filter(
        extract('year', Procurement.created_at) == today.year - 1
    ).scalar() or 0
    this_year_requests = db.query(func.count(Procurement.id)).filter(
        extract('year', Procurement.created_at) == today.year
    ).scalar() or 0
    growth = round(
        (this_year_requests - last_year_requests) / last_year_requests * 100, 2
    ) if last_year_requests else None

    return {
        "requests_today": requests_since(today),
        "requests_this_week": requests_since(week_start),
        "requests_this_month": requests_since(month_start),
        "requests_this_year": this_year_requests,
        "completed_orders_this_week": completed_this_week,
        "spending_this_month": spending_since(month_start),
        "spending_this_year": spending_since(year_start),
        "yearly_growth_percent": growth,
    }


def _pending_analytics_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_analytics_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_analytics_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_analytics_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_analytics_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_analytics_service_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_analytics_service_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
