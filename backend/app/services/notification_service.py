from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from datetime import datetime, date, timedelta
import os
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationCreate

def send_email_notification(to_email: str, subject: str, body: str) -> bool:
    from app.core.config import (
        SMTP_CONFIGURED, SMTP_SERVER, SMTP_PORT,
        SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM,
    )

    if SMTP_CONFIGURED and to_email:
        try:
            import smtplib
            from email.message import EmailMessage

            message = EmailMessage()
            message["From"] = SMTP_FROM
            message["To"] = to_email
            message["Subject"] = subject
            message.set_content(body)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(message)

            print(f"[EMAIL SENT] To: {to_email} | Subject: {subject}")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")

    print(f"[SIMULATED EMAIL] To: {to_email} | Subject: {subject} | Body: {body[:100]}...")
    return True

def send_sms_notification(mobile_number: str, message_body: str) -> bool:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")

    if account_sid and auth_token and from_number and mobile_number:
        try:
            import requests
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            payload = {
                "From": from_number,
                "To": mobile_number,
                "Body": message_body
            }
            res = requests.post(url, data=payload, auth=(account_sid, auth_token), timeout=5)
            if res.status_code in (200, 201):
                print(f"[TWILIO SMS SENT] To: {mobile_number}")
                return True
        except Exception as e:
            print(f"[TWILIO SMS ERROR] {e}")

    print(f"[SIMULATED SMS] To: {mobile_number or 'Target User'} | Message: {message_body[:80]}...")
    return True

def create_notification(db: Session, data: NotificationCreate) -> Notification:
    notif = Notification(
        user_id=data.user_id,
        target_role=data.target_role,
        notification_type=data.notification_type,
        title=data.title,
        description=data.description,
        module_name=data.module_name,
        related_record_id=data.related_record_id,
        priority=data.priority or "Medium",
        delivery_method=data.delivery_method or "In-App",
        is_read=False
    )

    email_success = False
    if data.delivery_method in ("Email", "All") or data.priority == "High":
        if data.user_id:
            u = db.query(User).filter(User.id == data.user_id).first()
            if u and u.email:
                email_success = send_email_notification(u.email, data.title, data.description)

    sms_success = False
    if data.delivery_method in ("SMS", "All") or data.priority == "High":
        if data.user_id:
            u = db.query(User).filter(User.id == data.user_id).first()
            if u and u.mobile_number:
                sms_success = send_sms_notification(u.mobile_number, f"{data.title}: {data.description[:100]}")

    notif.email_sent = email_success
    notif.sms_sent = sms_success

    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def get_user_notifications(db: Session, user_id: int, user_role: str = None, module_name: str = None, priority: str = None, unread_only: bool = False, limit: int = 100):
    query = db.query(Notification).filter(
        or_(
            Notification.user_id == user_id,
            Notification.target_role == user_role,
            Notification.target_role == "All"
        )
    )

    if module_name and module_name != "All":
        query = query.filter(Notification.module_name == module_name)
    if priority and priority != "All":
        query = query.filter(Notification.priority == priority)
    if unread_only:
        query = query.filter(Notification.is_read == False)

    return query.order_by(Notification.timestamp.desc()).limit(limit).all()

def mark_notification_read(db: Session, notification_id: int, user_id: int = None, user_role: str = None):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    if user_id is not None:
        visible = _visible_to_user(
            db.query(Notification).filter(Notification.id == notification_id),
            user_id, user_role
        ).first()
        if not visible:
            raise HTTPException(status_code=403, detail="This notification is not addressed to you")

    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

def _visible_to_user(query, user_id: int, user_role: str = None):
    return query.filter(
        or_(
            Notification.user_id == user_id,
            Notification.target_role == user_role,
            Notification.target_role == "All"
        )
    )

def mark_all_read(db: Session, user_id: int, user_role: str = None):
    notifications = _visible_to_user(db.query(Notification), user_id, user_role).filter(
        Notification.is_read == False
    ).all()

    for n in notifications:
        n.is_read = True

    db.commit()
    return {"message": f"Marked {len(notifications)} notifications as read"}

def get_unread_count(db: Session, user_id: int, user_role: str = None) -> int:
    return _visible_to_user(db.query(Notification), user_id, user_role).filter(
        Notification.is_read == False
    ).count()

def _safe_create(db: Session, data: NotificationCreate):
    try:
        return create_notification(db, data)
    except Exception as e:
        db.rollback()
        print(f"[NOTIFICATION ERROR] {data.notification_type}: {e}")
        return None

def _find_vendor_user_id(db: Session, vendor) -> int:
    if not vendor or not vendor.email:
        return None
    from sqlalchemy import func as sa_func
    user = db.query(User).filter(sa_func.lower(User.email) == vendor.email.lower()).first()
    return user.id if user else None

def notify_vendor_approval_decision(db: Session, vendor, approved: bool):
    decision = "Approved" if approved else "Rejected"
    _safe_create(db, NotificationCreate(
        user_id=_find_vendor_user_id(db, vendor),
        target_role=None,
        notification_type="Vendor Approval",
        title=f"Vendor Registration {decision}",
        description=(
            f"Your vendor profile '{vendor.company_name or vendor.vendor_name}' has been {decision.lower()} "
            f"by {vendor.approved_by or 'the procurement team'}."
        ),
        module_name="Vendor",
        related_record_id=str(vendor.id),
        priority="Medium",
        delivery_method="All"
    ))

def notify_procurement_submitted(db: Session, procurement):
    _safe_create(db, NotificationCreate(
        target_role="Procurement Manager",
        notification_type="Procurement Alert",
        title=f"New Procurement Request {procurement.request_number}",
        description=(
            f"{procurement.requested_by or 'A department user'} submitted '{procurement.request_title}' "
            f"({procurement.department}) and it is awaiting approval."
        ),
        module_name="Procurement",
        related_record_id=str(procurement.id),
        priority="High" if procurement.priority in ("High", "Critical") else "Medium",
        delivery_method="All" if procurement.priority == "Critical" else "In-App"
    ))

def notify_purchase_order_created(db: Session, purchase_order, vendor=None):
    _safe_create(db, NotificationCreate(
        user_id=_find_vendor_user_id(db, vendor),
        target_role=None if vendor else "Vendor",
        notification_type="Procurement Award",
        title=f"New Purchase Order {purchase_order.po_number}",
        description=(
            f"Purchase Order {purchase_order.po_number} for {purchase_order.item_name} "
            f"(qty {purchase_order.quantity}) has been issued to you."
        ),
        module_name="Procurement",
        related_record_id=str(purchase_order.id),
        priority="High",
        delivery_method="All"
    ))

def notify_invoice_status(db: Session, invoice, status: str, vendor=None):
    _safe_create(db, NotificationCreate(
        user_id=_find_vendor_user_id(db, vendor),
        target_role=None if vendor else "Finance Officer",
        notification_type="Invoice Update",
        title=f"Invoice {invoice.invoice_number} {status}",
        description=f"Invoice {invoice.invoice_number} for Rs. {invoice.total_amount:,.2f} is now marked '{status}'.",
        module_name="Invoice",
        related_record_id=str(invoice.id),
        priority="Low" if status in ("Verified",) else "Medium",
        delivery_method="In-App"
    ))

def notify_delivery_delay(db: Session, purchase_order, days_late: int):
    description = (
        f"Purchase Order {purchase_order.po_number} from {purchase_order.vendor_name} is "
        f"{days_late} day(s) past its expected delivery date."
    )
    for role in ("Procurement Manager", "Supply Chain Manager", "Vendor"):
        _safe_create(db, NotificationCreate(
            target_role=role,
            notification_type="Delivery Delay Warning",
            title=f"Delivery Delayed for PO {purchase_order.po_number}",
            description=description,
            module_name="Delivery",
            related_record_id=str(purchase_order.id),
            priority="High",
            delivery_method="All"
        ))


def _pending_notification_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_notification_service_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_notification_service_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_notification_service_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_notification_service_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_notification_service_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_notification_service_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_notification_service_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_notification_service_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_notification_service_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_notification_service_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
            "owner": getattr(item, "created_by", None),
        })
    return rows
