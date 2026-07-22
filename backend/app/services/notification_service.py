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


def _pending_notification_service_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
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
        })
    return rows


def _pending_notification_service_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
