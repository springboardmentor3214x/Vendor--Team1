from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from datetime import datetime
import os
import shutil

from app.models.communication import Communication
from app.models.discussion import Discussion
from app.models.shared_file import SharedFile
from app.models.activity_log import ActivityLog
from app.schemas.communication import CommunicationCreate
from app.schemas.discussion import DiscussionCreate


def log_activity(db: Session, user_name: str, action: str, module_name: str, related_record: str = None, user_id: int = None, details: str = None, ip_address: str = None):
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


def send_message(db: Session, data: CommunicationCreate, sender_id: int, sender_name: str, file: UploadFile = None):
    file_name = None
    file_path = None

    if file:
        upload_dir = os.path.join("static", "communications", str(data.vendor_id or 0))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_name = file.filename

    comm = Communication(
        vendor_id=data.vendor_id,
        procurement_id=data.procurement_id,
        po_id=data.po_id,
        contract_id=data.contract_id,
        discussion_id=data.discussion_id,
        sender_id=sender_id,
        sender_name=sender_name,
        receiver_id=data.receiver_id,
        receiver_name=data.receiver_name,
        message=data.message,
        is_read=False,
        file_name=file_name,
        file_path=file_path
    )
    db.add(comm)
    db.commit()
    db.refresh(comm)

    # Log Activity
    log_activity(db, sender_name, "Message Sent", "Communication", f"Vendor #{data.vendor_id or 'General'}", user_id=sender_id, details=f"Message: {data.message[:50]}")
    
    # Also save to shared_files if attachment is included
    if file:
        sf = SharedFile(
            file_name=file_name,
            file_path=file_path,
            file_type=file.content_type,
            uploaded_by=sender_name,
            vendor_id=data.vendor_id,
            procurement_id=data.procurement_id,
            po_id=data.po_id,
            contract_id=data.contract_id,
            discussion_id=data.discussion_id
        )
        db.add(sf)
        db.commit()

    return comm


def get_conversations(db: Session, vendor_id: int = None, po_id: int = None, contract_id: int = None, discussion_id: int = None):
    query = db.query(Communication)
    if vendor_id:
        query = query.filter(Communication.vendor_id == vendor_id)
    if po_id:
        query = query.filter(Communication.po_id == po_id)
    if contract_id:
        query = query.filter(Communication.contract_id == contract_id)
    if discussion_id:
        query = query.filter(Communication.discussion_id == discussion_id)

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


def upload_shared_file(db: Session, uploaded_by: str, file: UploadFile, vendor_id: int = None, procurement_id: int = None, po_id: int = None, contract_id: int = None, discussion_id: int = None):
    upload_dir = os.path.join("static", "shared_files", str(vendor_id or 0))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    sf = SharedFile(
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
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

    log_activity(db, uploaded_by, "File Uploaded", "Communication", f"File #{sf.id}", details=f"Filename: {file.filename}")
    return sf


def get_shared_files(db: Session, vendor_id: int = None, po_id: int = None, contract_id: int = None):
    query = db.query(SharedFile)
    if vendor_id:
        query = query.filter(SharedFile.vendor_id == vendor_id)
    if po_id:
        query = query.filter(SharedFile.po_id == po_id)
    if contract_id:
        query = query.filter(SharedFile.contract_id == contract_id)
    return query.order_by(SharedFile.created_at.desc()).all()


def get_activity_logs(db: Session, limit: int = 100, module_name: str = None):
    query = db.query(ActivityLog)
    if module_name and module_name != "All":
        query = query.filter(ActivityLog.module_name == module_name)
    return query.order_by(ActivityLog.timestamp.desc()).limit(limit).all()
