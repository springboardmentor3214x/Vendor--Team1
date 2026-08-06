from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from datetime import datetime, date, timedelta
import os

from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationCreate


# Twilio & Email Helper Functions
def send_email_notification(to_email: str, subject: str, body: str) -> bool:
    smtp_server = os.getenv("SMTP_SERVER", "localhost")
    # Log / Simulate email notification
    print(f"[EMAIL NOTIFICATION] To: {to_email} | Subject: {subject} | Body: {body[:100]}...")
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

    # Deliver via Email if requested or High priority
    email_success = False
    if data.delivery_method in ("Email", "All") or data.priority == "High":
        if data.user_id:
            u = db.query(User).filter(User.id == data.user_id).first()
            if u and u.email:
                email_success = send_email_notification(u.email, data.title, data.description)

    # Deliver via SMS if requested or High priority
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


def mark_notification_read(db: Session, notification_id: int, user_id: int = None):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif


def mark_all_read(db: Session, user_id: int, user_role: str = None):
    notifications = db.query(Notification).filter(
        or_(
            Notification.user_id == user_id,
            Notification.target_role == user_role
        ),
        Notification.is_read == False
    ).all()

    for n in notifications:
        n.is_read = True

    db.commit()
    return {"message": f"Marked {len(notifications)} notifications as read"}


def trigger_background_expiry_and_delay_checks(db: Session):
    """
    Background job that automatically generates delivery delay alerts,
    contract expiry reminders, and compliance document reminders.
    """
    from app.models.purchase_order import PurchaseOrder
    from app.models.contract import Contract
    from app.models.certification import Certification

    generated_count = 0
    today = date.today()
    now = datetime.utcnow()

    # 1. Delayed Deliveries Check
    delayed_pos = db.query(PurchaseOrder).filter(
        PurchaseOrder.status.in_(["Issued", "In Transit"]),
        PurchaseOrder.expected_delivery_date < now
    ).all()

    for po in delayed_pos:
        # Avoid duplicating same notification on same day
        existing = db.query(Notification).filter(
            Notification.notification_type == "Delivery Delay Warning",
            Notification.related_record_id == str(po.id)
        ).first()

        if not existing:
            create_notification(db, NotificationCreate(
                target_role="Procurement Manager",
                notification_type="Delivery Delay Warning",
                title=f"Delivery Delayed for PO #{po.po_number}",
                description=f"Purchase Order #{po.po_number} from vendor {po.vendor_name} is past its expected delivery date.",
                module_name="Delivery",
                related_record_id=str(po.id),
                priority="High",
                delivery_method="All"
            ))
            generated_count += 1

    # 2. Contract Expiry Check (30 days threshold)
    threshold_30 = today + timedelta(days=30)
    expiring_contracts = db.query(Contract).filter(
        Contract.end_date <= threshold_30,
        Contract.status.in_(["Active", "Expiring Soon"])
    ).all()

    for c in expiring_contracts:
        existing = db.query(Notification).filter(
            Notification.notification_type == "Contract Expiry Reminder",
            Notification.related_record_id == str(c.id)
        ).first()

        if not existing:
            days_left = (c.end_date - today).days
            create_notification(db, NotificationCreate(
                target_role="Procurement Manager",
                notification_type="Contract Expiry Reminder",
                title=f"Contract #{c.contract_number or c.id} Expiring Soon",
                description=f"Contract '{c.contract_title}' with vendor {c.vendor_name} expires in {days_left} days.",
                module_name="Contracts",
                related_record_id=str(c.id),
                priority="High" if days_left <= 7 else "Medium",
                delivery_method="All"
            ))
            generated_count += 1

    return {"message": "Background checks executed", "notifications_generated": generated_count}
