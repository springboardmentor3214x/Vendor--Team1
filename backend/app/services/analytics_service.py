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


def get_delivery_status_summary(db: Session) -> Dict[str, Any]:
    from app.models.order_tracking import OrderTracking

    now = datetime.utcnow()

    on_time = db.query(func.count(DeliveryPerformance.id)).filter(
        DeliveryPerformance.delivery_status.in_(["Delivered On Time", "Delivered Early"])
    ).scalar() or 0
    total_recorded = db.query(func.count(DeliveryPerformance.id)).scalar() or 0
    delayed = total_recorded - on_time

    pending_shipments = db.query(func.count(OrderTracking.id)).filter(
        OrderTracking.delivery_status == "Awaiting Shipment"
    ).scalar() or 0
    in_transit = db.query(func.count(OrderTracking.id)).filter(
        OrderTracking.delivery_status == "In Transit"
    ).scalar() or 0
    delivered = db.query(func.count(PurchaseOrder.id)).filter(
        PurchaseOrder.status == "Delivered"
    ).scalar() or 0
    completed = db.query(func.count(PurchaseOrder.id)).filter(
        PurchaseOrder.status == "Completed"
    ).scalar() or 0

    overdue = db.query(func.count(PurchaseOrder.id)).filter(
        PurchaseOrder.status.in_(ACTIVE_PO_STATUSES),
        PurchaseOrder.expected_delivery_date < now
    ).scalar() or 0

    return {
        "on_time_deliveries": on_time,
        "delayed_deliveries": delayed,
        "pending_shipments": pending_shipments,
        "in_transit": in_transit,
        "delivered_orders": delivered,
        "completed_deliveries": completed,
        "overdue_active_orders": overdue,
        "on_time_rate": round(on_time / total_recorded * 100, 2) if total_recorded else 0.0,
    }


def get_vendor_dashboard_analytics(db: Session, vendor_id: int) -> Dict[str, Any]:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        return None

    from app.services.performance_service import calculate_vendor_metrics
    metrics = calculate_vendor_metrics(db, vendor_id)

    total_orders = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id).count()
    active_pos = db.query(PurchaseOrder).filter(
        PurchaseOrder.vendor_id == vendor_id,
        PurchaseOrder.status.in_(ACTIVE_PO_STATUSES)
    ).count()
    completed_pos = db.query(PurchaseOrder).filter(
        PurchaseOrder.vendor_id == vendor_id,
        PurchaseOrder.status.in_(COMPLETED_PO_STATUSES)
    ).count()

    active_contracts = db.query(Contract).filter(Contract.vendor_id == vendor_id, Contract.status == "Active").count()
    expiring_contracts = db.query(Contract).filter(Contract.vendor_id == vendor_id, Contract.status == "Expiring Soon").count()

    recent_msgs = db.query(Communication).filter(Communication.vendor_id == vendor_id).order_by(Communication.sent_at.desc()).limit(5).all()
    msg_summary = [
        {
            "id": m.id,
            "sender_name": m.sender_name,
            "message": m.message[:60],
            "sent_at": m.sent_at,
            "is_read": m.is_read
        }
        for m in recent_msgs
    ]

    total_invoiced = db.query(func.sum(Invoice.total_amount)).filter(Invoice.vendor_id == vendor_id).scalar() or 0.0
    paid_invoiced = db.query(func.sum(Invoice.total_amount)).filter(Invoice.vendor_id == vendor_id, Invoice.payment_status == "Paid").scalar() or 0.0

    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.vendor_name,
        "company_name": vendor.company_name,
        "category": vendor.category,
        "reliability_score": vendor.reliability_score or 0.0,
        "delivery_score": vendor.delivery_score or 0.0,
        "quality_score": vendor.quality_score or 0.0,
        "communication_score": vendor.communication_score or 0.0,
        "service_score": vendor.service_score or 0.0,
        "summary": {
            "total_orders": total_orders,
            "active_pos": active_pos,
            "completed_orders": completed_pos,
            "active_contracts": active_contracts,
            "expiring_contracts": expiring_contracts,
            "total_invoiced": float(total_invoiced),
            "total_paid": float(paid_invoiced)
        },
        "performance_metrics": metrics,
        "recent_communications": msg_summary
    }


def _vendor_monthly_spend(db: Session, vendor_id: int, months: int = 12) -> List[Dict[str, Any]]:
    today = date.today()
    trends = []
    for i in range(months - 1, -1, -1):
        target_month = (today.month - i - 1) % 12 + 1
        target_year = today.year if today.month - i > 0 else today.year - 1
        month_name = date(target_year, target_month, 1).strftime("%b %Y")

        spend = db.query(func.sum(Procurement.total_price)).filter(
            Procurement.vendor_id == vendor_id,
            extract('year', Procurement.created_at) == target_year,
            extract('month', Procurement.created_at) == target_month
        ).scalar() or 0.0
        count = db.query(func.count(Procurement.id)).filter(
            Procurement.vendor_id == vendor_id,
            extract('year', Procurement.created_at) == target_year,
            extract('month', Procurement.created_at) == target_month
        ).scalar() or 0

        trends.append({"month": month_name, "total_spending": float(spend), "request_count": count})
    return trends


def _vendor_delivery_breakdown(db: Session, vendor_id: int) -> Dict[str, int]:
    rows = db.query(
        DeliveryPerformance.delivery_status, func.count(DeliveryPerformance.id)
    ).filter(DeliveryPerformance.vendor_id == vendor_id).group_by(
        DeliveryPerformance.delivery_status
    ).all()
    return {(status or "Unknown"): count for status, count in rows}


def get_vendor_analytics(db: Session, vendor_id: int) -> Dict[str, Any]:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        return None

    from app.services import reliability_service

    dashboard = get_vendor_dashboard_analytics(db, vendor_id)
    reliability = reliability_service.get_vendor_reliability_details(db, vendor_id)
    trends = reliability_service.get_performance_trends(db, vendor_id)

    contract_rows = db.query(Contract.status, func.count(Contract.id)).filter(
        Contract.vendor_id == vendor_id
    ).group_by(Contract.status).all()
    contract_breakdown = {(status or "Unknown"): count for status, count in contract_rows}

    invoice_rows = db.query(Invoice.payment_status, func.count(Invoice.id)).filter(
        Invoice.vendor_id == vendor_id
    ).group_by(Invoice.payment_status).all()
    invoice_breakdown = {(status or "Unknown"): count for status, count in invoice_rows}

    return {
        "vendor_id": vendor.id,
        "vendor_name": vendor.vendor_name,
        "company_name": vendor.company_name,
        "category": vendor.category,
        "status": vendor.status,
        "approval_status": vendor.approval_status,
        "dashboard": dashboard,
        "reliability": reliability,
        "performance_trends": trends,
        "monthly_spend": _vendor_monthly_spend(db, vendor_id),
        "delivery_breakdown": _vendor_delivery_breakdown(db, vendor_id),
        "contract_breakdown": contract_breakdown,
        "invoice_breakdown": invoice_breakdown,
    }


def get_admin_dashboard_analytics(db: Session) -> Dict[str, Any]:
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.account_status == "Active").count()
    total_vendors = db.query(Vendor).count()
    approved_vendors = db.query(Vendor).filter(Vendor.approval_status == "Approved").count()
    pending_vendors = db.query(Vendor).filter(Vendor.approval_status == "Pending").count()
    blocked_vendors = db.query(Vendor).filter(Vendor.status == "Blocked").count()

    total_contracts = db.query(Contract).count()
    active_contracts = db.query(Contract).filter(Contract.status == "Active").count()
    expiring_contracts = db.query(Contract).filter(Contract.status == "Expiring Soon").count()
    expired_contracts = db.query(Contract).filter(Contract.status == "Expired").count()

    total_procurements = db.query(Procurement).count()
    total_pos = db.query(PurchaseOrder).count()

    comp_records = db.query(ComplianceRecord).count()
    compliant_count = db.query(ComplianceRecord).filter(ComplianceRecord.status == "Compliant").count()

    return {
        "user_analytics": {
            "total_users": total_users,
            "active_users": active_users,
            "pending_users": total_users - active_users
        },
        "vendor_analytics": {
            "total_vendors": total_vendors,
            "approved_vendors": approved_vendors,
            "pending_vendors": pending_vendors,
            "blocked_vendors": blocked_vendors
        },
        "contract_analytics": {
            "total_contracts": total_contracts,
            "active_contracts": active_contracts,
            "expiring_contracts": expiring_contracts,
            "expired_contracts": expired_contracts
        },
        "procurement_analytics": {
            "total_procurement_requests": total_procurements,
            "total_purchase_orders": total_pos
        },
        "compliance_analytics": {
            "total_compliance_records": comp_records,
            "compliant_count": compliant_count,
            "compliance_percentage": round((compliant_count / comp_records * 100), 2) if comp_records > 0 else 100.0
        },
        "system_statistics": get_system_statistics(db),
    }


def get_system_statistics(db: Session) -> Dict[str, Any]:
    from app.models.activity_log import ActivityLog
    from app.models.notification import Notification

    now = datetime.utcnow()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)

    users_by_role = dict(
        db.query(User.role, func.count(User.id)).group_by(User.role).all()
    )

    return {
        "users_by_role": {role: count for role, count in users_by_role.items()},
        "activity_last_24h": db.query(func.count(ActivityLog.id)).filter(
            ActivityLog.timestamp >= last_24h
        ).scalar() or 0,
        "activity_last_7d": db.query(func.count(ActivityLog.id)).filter(
            ActivityLog.timestamp >= last_7d
        ).scalar() or 0,
        "total_messages": db.query(func.count(Communication.id)).scalar() or 0,
        "unread_notifications": db.query(func.count(Notification.id)).filter(
            Notification.is_read == False
        ).scalar() or 0,
        "total_invoices": db.query(func.count(Invoice.id)).scalar() or 0,
        "total_certifications": db.query(func.count(Certification.id)).scalar() or 0,
        "expired_certifications": db.query(func.count(Certification.id)).filter(
            Certification.expiry_date < date.today()
        ).scalar() or 0,
    }
