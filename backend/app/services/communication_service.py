from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, UploadFile
from datetime import datetime
from typing import Optional
import os
import shutil

from app.models.communication import Communication
from app.models.discussion import Discussion
from app.models.shared_file import SharedFile
from app.models.activity_log import ActivityLog
from app.models.notification import Notification
from app.models.user import User
from app.schemas.communication import CommunicationCreate
from app.schemas.discussion import DiscussionCreate
from app.utils.uploads import (
    validate_upload,
    ALLOWED_SHARED_FILE_EXTENSIONS,
    MAX_SHARED_FILE_SIZE_BYTES,
)


def unique_upload_path(upload_dir: str, filename: str) -> tuple:
    safe_filename = os.path.basename(filename)
    stem, extension = os.path.splitext(safe_filename)
    candidate = safe_filename
    counter = 1

    while os.path.exists(os.path.join(upload_dir, candidate)):
        candidate = f"{stem} ({counter}){extension}"
        counter += 1

    return candidate, os.path.join(upload_dir, candidate)


def log_activity(db: Session, user_name: str, action: str, module_name: str, related_record: str = None, user_id: int = None, details: str = None, ip_address: str = None):
    try:
        log = ActivityLog(
            user_id=user_id,
            user_name=user_name,
            action=action,
            module_name=module_name,
            related_record=related_record,
            ip_address=ip_address or "127.0.0.1",
            details=details
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        print(f"Log activity notice: {e}")
        return None


def send_message(db: Session, data: CommunicationCreate, sender_id: int, sender_name: str, file: UploadFile = None):
    file_name = None
    file_path = None

    file_size = 0
    if file and file.filename:
        contents = validate_upload(file, ALLOWED_SHARED_FILE_EXTENSIONS, MAX_SHARED_FILE_SIZE_BYTES)
        file_size = len(contents)
        upload_dir = os.path.join("static", "communications", str(data.vendor_id or sender_id or 0))
        os.makedirs(upload_dir, exist_ok=True)
        file_name, file_path = unique_upload_path(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

    receiver_name = data.receiver_name
    if data.receiver_id and not receiver_name:
        rx_user = db.query(User).filter(User.id == data.receiver_id).first()
        if rx_user:
            receiver_name = rx_user.name

    comm = Communication(
        vendor_id=data.vendor_id,
        procurement_id=data.procurement_id,
        po_id=data.po_id,
        contract_id=data.contract_id,
        discussion_id=data.discussion_id,
        sender_id=sender_id,
        sender_name=sender_name,
        receiver_id=data.receiver_id,
        receiver_name=receiver_name,
        message=data.message,
        is_read=False,
        file_name=file_name,
        file_path=file_path
    )
    db.add(comm)
    db.commit()
    db.refresh(comm)

    recipient_desc = f"User #{data.receiver_id} ({receiver_name})" if data.receiver_id else f"Vendor #{data.vendor_id or 'General'}"
    log_activity(db, sender_name, "Message Sent", "Communication", recipient_desc, user_id=sender_id, details=f"Message: {data.message[:50]}")

    try:
        notif_user_id = data.receiver_id
        target_role = None if data.receiver_id else "Procurement Manager"
        notif = Notification(
            user_id=notif_user_id,
            target_role=target_role,
            notification_type="Direct Message",
            title=f"New Message from {sender_name}",
            description=f"{sender_name}: {data.message[:80]}...",
            module_name="Communication",
            priority="High" if data.receiver_id else "Medium",
            is_read=False
        )
        db.add(notif)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Notification logging notice: {e}")

    if file_name:
        try:
            sf = SharedFile(
                file_name=file_name,
                file_path=file_path,
                file_type=file.content_type,
                file_size=file_size,
                uploaded_by=sender_name,
                vendor_id=data.vendor_id,
                procurement_id=data.procurement_id,
                po_id=data.po_id,
                contract_id=data.contract_id,
                discussion_id=data.discussion_id
            )
            db.add(sf)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Shared file logging notice: {e}")

    return comm


def get_conversations(
    db: Session,
    vendor_id: Optional[int] = None,
    po_id: Optional[int] = None,
    contract_id: Optional[int] = None,
    discussion_id: Optional[int] = None,
    user_id: Optional[int] = None,
    receiver_id: Optional[int] = None
):
    query = db.query(Communication)
    if vendor_id:
        query = query.filter(Communication.vendor_id == vendor_id)
    if po_id:
        query = query.filter(Communication.po_id == po_id)
    if contract_id:
        query = query.filter(Communication.contract_id == contract_id)
    if discussion_id:
        query = query.filter(Communication.discussion_id == discussion_id)

    if receiver_id and user_id:
        query = query.filter(
            or_(
                (Communication.sender_id == user_id) & (Communication.receiver_id == receiver_id),
                (Communication.sender_id == receiver_id) & (Communication.receiver_id == user_id)
            )
        )
    elif user_id:
        query = query.filter(
            or_(
                Communication.sender_id == user_id,
                Communication.receiver_id == user_id
            )
        )
    elif receiver_id:
        query = query.filter(Communication.receiver_id == receiver_id)

    return query.order_by(Communication.sent_at.asc()).all()


def create_discussion(db: Session, data: DiscussionCreate, created_by: str, user_id: int = None):
    disc = Discussion(
        topic=data.topic,
        vendor_id=data.vendor_id,
        procurement_id=data.procurement_id,
        po_id=data.po_id,
        contract_id=data.contract_id,
        created_by=created_by,
        status="Active"
    )
    db.add(disc)
    db.commit()
    db.refresh(disc)

    log_activity(db, created_by, "Discussion Created", "Communication", f"Discussion #{disc.id}", user_id=user_id, details=f"Topic: {data.topic}")
    return disc


def get_discussions(db: Session, vendor_id: int = None, po_id: int = None):
    query = db.query(Discussion)
    if vendor_id:
        query = query.filter(Discussion.vendor_id == vendor_id)
    if po_id:
        query = query.filter(Discussion.po_id == po_id)
    return query.order_by(Discussion.created_at.desc()).all()


def upload_shared_file(db: Session, uploaded_by: str, file: UploadFile, vendor_id: int = None, procurement_id: int = None, po_id: int = None, contract_id: int = None, discussion_id: int = None, user_id: int = None):
    contents = validate_upload(file, ALLOWED_SHARED_FILE_EXTENSIONS, MAX_SHARED_FILE_SIZE_BYTES)

    upload_dir = os.path.join("static", "shared_files", str(vendor_id or 0))
    os.makedirs(upload_dir, exist_ok=True)
    safe_filename, file_path = unique_upload_path(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    sf = SharedFile(
        file_name=safe_filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=len(contents),
        uploaded_by=uploaded_by,
        vendor_id=vendor_id,
        procurement_id=procurement_id,
        po_id=po_id,
        contract_id=contract_id,
        discussion_id=discussion_id
    )
    db.add(sf)
    db.commit()
    db.refresh(sf)

    log_activity(db, uploaded_by, "File Uploaded", "Communication", f"File #{sf.id}", user_id=user_id, details=f"Filename: {safe_filename}")
    return sf


def mark_messages_read(db: Session, user_id: int, message_ids: Optional[list] = None,
                       vendor_id: Optional[int] = None, discussion_id: Optional[int] = None,
                       user_name: str = "User"):
    query = db.query(Communication).filter(
        Communication.is_read == False,
        Communication.sender_id != user_id
    )
    if message_ids:
        query = query.filter(Communication.id.in_(message_ids))
    if vendor_id:
        query = query.filter(Communication.vendor_id == vendor_id)
    if discussion_id:
        query = query.filter(Communication.discussion_id == discussion_id)

    messages = query.all()
    for m in messages:
        m.is_read = True
    db.commit()

    if messages:
        log_activity(db, user_name, "Message Viewed", "Communication",
                     f"{len(messages)} message(s)", user_id=user_id)

    return {"message": f"Marked {len(messages)} message(s) as read", "count": len(messages)}


def get_unread_message_count(db: Session, user_id: int, vendor_id: Optional[int] = None) -> int:
    query = db.query(Communication).filter(
        Communication.is_read == False,
        Communication.sender_id != user_id
    )
    if vendor_id:
        query = query.filter(
            or_(Communication.vendor_id == vendor_id, Communication.receiver_id == user_id)
        )
    else:
        query = query.filter(Communication.receiver_id == user_id)
    return query.count()


def get_shared_files(db: Session, vendor_id: int = None, po_id: int = None, contract_id: int = None,
                     procurement_id: int = None, discussion_id: int = None):
    query = db.query(SharedFile)
    if vendor_id:
        query = query.filter(SharedFile.vendor_id == vendor_id)
    if po_id:
        query = query.filter(SharedFile.po_id == po_id)
    if contract_id:
        query = query.filter(SharedFile.contract_id == contract_id)
    if procurement_id:
        query = query.filter(SharedFile.procurement_id == procurement_id)
    if discussion_id:
        query = query.filter(SharedFile.discussion_id == discussion_id)
    return query.order_by(SharedFile.created_at.desc()).all()


def get_activity_logs(db: Session, limit: int = 100, module_name: str = None):
    query = db.query(ActivityLog)
    if module_name and module_name != "All":
        query = query.filter(ActivityLog.module_name == module_name)
    return query.order_by(ActivityLog.timestamp.desc()).limit(limit).all()
