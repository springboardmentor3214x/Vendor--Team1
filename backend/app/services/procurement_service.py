from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, or_
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, List

from app.models.procurement import Procurement
from app.models.procurement_approval import ProcurementApproval
from app.models.procurement_status_history import ProcurementStatusHistory
from app.models.purchase_order import PurchaseOrder
from app.models.invoice import Invoice
from app.schemas.procurement import ProcurementCreate
from app.models.delivery_performance import DeliveryPerformance
from app.models.vendor import Vendor
from app.services.vendor_service import update_vendor_scores
from app.utils.delivery_timing import delivery_status_from_times
from app.core.risk import (
    calculate_risk_level, vendor_has_performance_data,
    HIGH_RISK, MEDIUM_RISK, NOT_RATED,
)


def record_status_history(db: Session, procurement_id: int, status: str, updated_by: str, remarks: Optional[str] = None, po_id: Optional[int] = None):
    try:
        hist = ProcurementStatusHistory(
            procurement_id=procurement_id,
            po_id=po_id,
            status=status,
            updated_by=updated_by,
            remarks=remarks
        )
        db.add(hist)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to record status history: {e}")


def record_approval(db: Session, procurement_id: int, action: str, action_by: str, remarks: Optional[str] = None):
    try:
        appr = ProcurementApproval(
            procurement_id=procurement_id,
            action=action,
            action_by=action_by,
            remarks=remarks
        )
        db.add(appr)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to record approval: {e}")


def generate_request_number(db: Session) -> str:
    year = datetime.utcnow().year
    prefix = f"PR-{year}-"
    last = (
        db.query(Procurement.request_number)
        .filter(Procurement.request_number.like(f"{prefix}%"))
        .order_by(Procurement.request_number.desc())
        .first()
    )
    next_seq = 1
    if last and last[0]:
        try:
            next_seq = int(last[0].rsplit("-", 1)[1]) + 1
        except (ValueError, IndexError):
            next_seq = db.query(func.count(Procurement.id)).scalar() + 1

    while db.query(Procurement).filter(Procurement.request_number == f"{prefix}{next_seq:04d}").first():
        next_seq += 1
    return f"{prefix}{next_seq:04d}"


def create_procurement(db: Session, data: ProcurementCreate):
    if data.expected_delivery_date and (data.status or "Pending") != "Draft":
        requested = data.expected_delivery_date
        today = datetime.utcnow().date()
        if requested.tzinfo is not None:
            requested = requested.replace(tzinfo=None)
        if requested.date() < today:
            raise HTTPException(
                status_code=400,
                detail="Required Delivery Date cannot be in the past"
            )

    unit_price = data.unit_price or 0.0
    if data.estimated_budget and data.quantity > 0 and unit_price == 0.0:
        unit_price = data.estimated_budget / data.quantity
    total_price = data.estimated_budget if data.estimated_budget is not None else (data.quantity * unit_price)

    req_num = generate_request_number(db)
    init_status = data.status or "Pending"

    proc = Procurement(
        request_number=req_num,
        request_title=data.request_title or f"Request for {data.item_name}",
        department=data.department or "General",
        requested_by=data.requested_by or "Department User",
        item_name=data.item_name,
        category=data.category or "General",
        vendor_id=data.vendor_id,
        quantity=data.quantity,
        unit_of_measurement=data.unit_of_measurement or "Units",
        unit_price=unit_price,
        total_price=total_price,
        priority=data.priority or "Medium",
        business_justification=data.business_justification,
        remarks=data.remarks,
        supporting_document=data.supporting_document,
        expected_delivery_date=data.expected_delivery_date,
        status=init_status,
        approval_status="Pending" if init_status != "Draft" else "Draft"
    )
    try:
        db.add(proc)
        db.commit()
        db.refresh(proc)

        record_status_history(db, proc.id, init_status, proc.requested_by, "Procurement Request Created")
        return proc
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_procurements(
    db: Session,
    department: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    keyword: Optional[str] = None
):
    query = db.query(Procurement)
    if department:
        query = query.filter(Procurement.department.ilike(f"%{department}%"))
    if status:
        query = query.filter(Procurement.status == status)
    if priority:
        query = query.filter(Procurement.priority == priority)
    if keyword:
        pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Procurement.request_number.ilike(pattern),
                Procurement.request_title.ilike(pattern),
                Procurement.item_name.ilike(pattern),
                Procurement.department.ilike(pattern),
                Procurement.requested_by.ilike(pattern)
            )
        )
    return query.order_by(Procurement.created_at.desc()).all()


def get_procurement(db: Session, procurement_id: int):
    return db.query(Procurement).filter(Procurement.id == procurement_id).first()


def update_procurement(db: Session, procurement_id: int, data: ProcurementCreate):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("Pending", "Draft", "Modification Required"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot edit procurement in '{proc.status}' status. Only Pending/Draft/Modification Required requests can be modified."
        )
    unit_price = data.unit_price or proc.unit_price
    if data.estimated_budget and data.quantity > 0:
        total_price = data.estimated_budget
        unit_price = total_price / data.quantity
    else:
        total_price = data.quantity * unit_price

    if data.request_title:
        proc.request_title = data.request_title
    if data.department:
        proc.department = data.department
    if data.requested_by:
        proc.requested_by = data.requested_by
    proc.item_name = data.item_name
    if data.category:
        proc.category = data.category
    if data.vendor_id:
        proc.vendor_id = data.vendor_id
    proc.quantity = data.quantity
    if data.unit_of_measurement:
        proc.unit_of_measurement = data.unit_of_measurement
    proc.unit_price = unit_price
    proc.total_price = total_price
    if data.priority:
        proc.priority = data.priority
    if data.business_justification:
        proc.business_justification = data.business_justification
    if data.remarks:
        proc.remarks = data.remarks
    if data.supporting_document:
        proc.supporting_document = data.supporting_document
    if data.expected_delivery_date:
        proc.expected_delivery_date = data.expected_delivery_date
    if data.status and data.status != proc.status:
        proc.status = data.status

    db.commit()
    db.refresh(proc)
    record_status_history(db, proc.id, proc.status, proc.requested_by or "User", "Procurement Request Updated")
    return proc


def delete_procurement(db: Session, procurement_id: int):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    active_po = db.query(PurchaseOrder).filter(
        PurchaseOrder.procurement_id == procurement_id,
        PurchaseOrder.status.in_(["Issued", "In Transit", "Pending"])
    ).first()
    if active_po:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete procurement with active Purchase Order #{active_po.po_number}. Complete or cancel the PO first."
        )
    unpaid_invoice = db.query(Invoice).filter(
        Invoice.procurement_id == procurement_id,
        Invoice.payment_status.in_(["Pending", "Verified", "Approved"])
    ).first()
    if unpaid_invoice:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete procurement with unpaid Invoice #{unpaid_invoice.invoice_number}. Settle the invoice first."
        )
    if proc.status not in ("Pending", "Draft", "Cancelled", "Modification Required"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete procurement in '{proc.status}' status. Only Pending, Draft, Modification Required or Cancelled requests can be deleted."
        )
    db.delete(proc)
    db.commit()
    return proc


def approve_procurement(db: Session, procurement_id: int, approved_by: str, remarks: Optional[str] = "Approved"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("Pending", "Modification Required"):
        raise HTTPException(status_code=400, detail="Only pending or modification required requests can be approved")
    proc.approval_status = "Approved"
    proc.status = "Approved"
    proc.approved_by = approved_by
    if remarks:
        proc.remarks = remarks
    db.commit()
    db.refresh(proc)

    record_approval(db, proc.id, "Approved", approved_by, remarks)
    record_status_history(db, proc.id, "Approved", approved_by, remarks)
    return proc


def reject_procurement(db: Session, procurement_id: int, approved_by: str, remarks: Optional[str] = "Rejected"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("Pending", "Modification Required"):
        raise HTTPException(status_code=400, detail="Only pending requests can be rejected")
    proc.approval_status = "Rejected"
    proc.status = "Cancelled"
    proc.approved_by = approved_by
    if remarks:
        proc.remarks = remarks
    db.commit()
    db.refresh(proc)

    record_approval(db, proc.id, "Rejected", approved_by, remarks)
    record_status_history(db, proc.id, "Cancelled", approved_by, remarks)
    return proc


def send_back_procurement(db: Session, procurement_id: int, user_name: str, remarks: Optional[str] = "Needs modification"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending requests can be sent back for modification")
    proc.approval_status = "Modification Required"
    proc.status = "Modification Required"
    if remarks:
        proc.remarks = remarks
    db.commit()
    db.refresh(proc)

    record_approval(db, proc.id, "Modification Required", user_name, remarks)
    record_status_history(db, proc.id, "Modification Required", user_name, remarks)
    return proc


def assign_vendor(db: Session, procurement_id: int, vendor_id: int, user_name: str = "Procurement Manager",
                  acknowledge_risk: bool = False):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("Approved", "Pending", "Vendor Assigned"):
        raise HTTPException(status_code=400, detail="Vendor can only be assigned on approved requests")
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if vendor.approval_status != "Approved":
        raise HTTPException(status_code=400, detail=f"Cannot assign vendor '{vendor.vendor_name}' — vendor is not approved (status: {vendor.approval_status})")
    if vendor.status not in ("Active",):
        raise HTTPException(status_code=400, detail=f"Cannot assign vendor '{vendor.vendor_name}' — vendor is {vendor.status}")
    risk_level = calculate_risk_level(
        vendor.reliability_score,
        vendor_has_performance_data(db, vendor_id)
    )
    if risk_level == HIGH_RISK and not acknowledge_risk:
        raise HTTPException(
            status_code=409,
            detail=(
                f"'{vendor.company_name or vendor.vendor_name}' is a HIGH RISK vendor "
                f"(reliability score {vendor.reliability_score:.1f}). Assigning this vendor requires "
                f"explicit confirmation from a Procurement Manager or Administrator."
            )
        )

    proc.vendor_id = vendor_id
    proc.status = "Vendor Assigned"
    proc.approval_status = "Approved"
    db.commit()
    db.refresh(proc)

    remark = f"Assigned to vendor: {vendor.company_name or vendor.vendor_name}"
    if risk_level == HIGH_RISK:
        remark += " (HIGH RISK vendor — assignment explicitly confirmed)"
    record_status_history(db, proc.id, "Vendor Assigned", user_name, remark)

    warning = None
    if risk_level == HIGH_RISK:
        warning = (
            f"{vendor.company_name or vendor.vendor_name} is classified HIGH RISK "
            f"(reliability {vendor.reliability_score:.1f}). Monitor this order closely."
        )
    elif risk_level == MEDIUM_RISK:
        warning = (
            f"{vendor.company_name or vendor.vendor_name} is classified MEDIUM RISK "
            f"(reliability {vendor.reliability_score:.1f})."
        )
    elif risk_level == NOT_RATED:
        warning = (
            f"{vendor.company_name or vendor.vendor_name} has no performance history yet, "
            f"so no reliability rating is available. Monitor this first order closely."
        )

    return proc, risk_level, warning


def place_order(db: Session, procurement_id: int, user_name: str = "Procurement Manager"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("Approved", "Vendor Assigned"):
        raise HTTPException(status_code=400, detail="Only approved requests with assigned vendor can be ordered")
    proc.status = "Ordered"
    db.commit()
    db.refresh(proc)

    record_status_history(db, proc.id, "Ordered", user_name, "Purchase Order Issued")
    return proc


def filter_procurements(db: Session, status: str):
    return db.query(Procurement).filter(Procurement.status == status).all()


def search_procurements(db: Session, keyword: str):
    pattern = f"%{keyword}%"
    return db.query(Procurement).filter(
        or_(
            Procurement.request_number.ilike(pattern),
            Procurement.request_title.ilike(pattern),
            Procurement.item_name.ilike(pattern)
        )
    ).all()


def mark_delivered(db: Session, procurement_id: int, actual_time: Optional[datetime] = None, user_name: str = "Supply Chain Manager"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status not in ("In Transit", "Ordered"):
        raise HTTPException(status_code=400, detail="Order must be ordered or in transit before delivery")
    proc.status = "Delivered"
    proc.actual_delivery_date = actual_time or datetime.utcnow()

    expected = proc.expected_delivery_date or proc.actual_delivery_date
    status, delay_hours, delay_days = delivery_status_from_times(expected, proc.actual_delivery_date)

    delivery = DeliveryPerformance(
        procurement_id=proc.id,
        vendor_id=proc.vendor_id,
        expected_date=expected,
        actual_date=proc.actual_delivery_date,
        delay_days=delay_days,
        delay_hours=delay_hours,
        delivery_status=status,
        remarks="Recorded when marked delivered"
    )
    db.add(delivery)
    db.commit()

    if proc.vendor_id:
        try:
            update_vendor_scores(db, proc.vendor_id)
        except Exception as e:
            print(f"Failed to update vendor scores: {e}")

    db.refresh(proc)
    record_status_history(db, proc.id, "Delivered", user_name, "Order items delivered to warehouse")
    return proc


def dispatch_procurement(db: Session, procurement_id: int, user_name: str = "Vendor"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status != "Ordered":
        raise HTTPException(status_code=400, detail="Only ordered purchase orders can be dispatched")
    proc.status = "In Transit"
    db.commit()
    db.refresh(proc)

    record_status_history(db, proc.id, "In Transit", user_name, "Order dispatched by vendor")
    return proc


def mark_completed(db: Session, procurement_id: int, user_name: str = "Finance Officer"):
    proc = get_procurement(db, procurement_id)
    if not proc:
        return None
    if proc.status != "Delivered":
        raise HTTPException(status_code=400, detail="Only delivered orders can be marked completed")
    proc.status = "Completed"
    db.commit()
    db.refresh(proc)

    record_status_history(db, proc.id, "Completed", user_name, "Invoice verified and payment processed")
    return proc


def get_procurements_by_vendor(db: Session, vendor_id: int):
    return db.query(Procurement).filter(Procurement.vendor_id == vendor_id).all()


def get_status_history(db: Session, procurement_id: int):
    return db.query(ProcurementStatusHistory).filter(ProcurementStatusHistory.procurement_id == procurement_id).order_by(ProcurementStatusHistory.created_at.desc()).all()


def procurement_dashboard(db: Session):
    total = db.query(Procurement).count()
    pending = db.query(Procurement).filter(Procurement.status == "Pending").count()
    approved = db.query(Procurement).filter(Procurement.status.in_(["Approved", "Vendor Assigned"])).count()
    po_created = db.query(PurchaseOrder).count()
    delivered = db.query(Procurement).filter(Procurement.status == "Delivered").count()
    completed = db.query(Procurement).filter(Procurement.status == "Completed").count()
    cancelled = db.query(Procurement).filter(Procurement.status == "Cancelled").count()

    recent_history = db.query(ProcurementStatusHistory).order_by(ProcurementStatusHistory.created_at.desc()).limit(8).all()
    recent_activities = []
    for h in recent_history:
        proc = db.query(Procurement).filter(Procurement.id == h.procurement_id).first()
        pr_title = proc.request_title if proc else f"Request #{h.procurement_id}"
        recent_activities.append({
            "message": f"{pr_title}: status updated to '{h.status}' by {h.updated_by}",
            "status": h.status,
            "timestamp": h.created_at.strftime("%b %d, %H:%M") if h.created_at else ""
        })

    if not recent_activities:
        recent_activities = [
            {"message": "System ready for procurement request processing", "status": "Info", "timestamp": "Now"}
        ]

    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "po_created": po_created,
        "delivered": delivered,
        "completed": completed,
        "cancelled": cancelled,
        "recent_activities": recent_activities
    }
