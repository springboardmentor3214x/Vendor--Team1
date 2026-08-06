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


def get_procurement_manager_dashboard_analytics(db: Session) -> Dict[str, Any]:
    total_requests = db.query(Procurement).count()
    pending_approvals = db.query(Procurement).filter(Procurement.approval_status == "Pending").count()
    active_pos = db.query(PurchaseOrder).filter(PurchaseOrder.status.in_(["Issued", "In Transit"])).count()
    completed_orders = db.query(Procurement).filter(Procurement.status == "Completed").count()
    cancelled_orders = db.query(Procurement).filter(Procurement.status == "Rejected").count()

    # Total Procurement Expenditure
    total_cost_res = db.query(func.sum(Procurement.total_price)).scalar() or 0.0
    total_po_cost = db.query(func.sum(PurchaseOrder.total_cost)).scalar() or 0.0

    # Expenses by Department
    dept_spending = db.query(
        Procurement.department, func.sum(Procurement.total_price), func.count(Procurement.id)
    ).group_by(Procurement.department).all()

    department_breakdown = [
        {"department": dept or "General", "total_spending": float(spend or 0.0), "request_count": count}
        for dept, spend, count in dept_spending
    ]

    # Category Breakdown
    cat_spending = db.query(
        Procurement.category, func.sum(Procurement.total_price), func.count(Procurement.id)
    ).group_by(Procurement.category).all()

    category_breakdown = [
        {"category": cat or "General", "total_spending": float(spend or 0.0), "request_count": count}
        for cat, spend, count in cat_spending
    ]

    # Monthly Expenditure Trends (Last 6 Months)
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

    # Active Purchase Orders list
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
            "total_expenditure": float(total_cost_res)
        },
        "department_breakdown": department_breakdown,
        "category_breakdown": category_breakdown,
        "monthly_trends": monthly_trends,
        "active_purchase_orders_list": po_summary
    }


def get_vendor_dashboard_analytics(db: Session, vendor_id: int) -> Dict[str, Any]:
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        return None

    from app.services.performance_service import calculate_vendor_metrics
    metrics = calculate_vendor_metrics(db, vendor_id)

    total_orders = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id).count()
    active_pos = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id, PurchaseOrder.status.in_(["Issued", "In Transit"])).count()
    completed_pos = db.query(PurchaseOrder).filter(PurchaseOrder.vendor_id == vendor_id, PurchaseOrder.status == "Delivered").count()

    # Active Contracts
    active_contracts = db.query(Contract).filter(Contract.vendor_id == vendor_id, Contract.status == "Active").count()
    expiring_contracts = db.query(Contract).filter(Contract.vendor_id == vendor_id, Contract.status == "Expiring Soon").count()

    # Recent Messages
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

    # Invoices & Payments
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
        }
    }
