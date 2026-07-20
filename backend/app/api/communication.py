from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.communication import CommunicationCreate, CommunicationResponse
from app.schemas.discussion import DiscussionCreate, DiscussionResponse
from app.schemas.shared_file import SharedFileResponse
from app.schemas.activity_log import ActivityLogResponse
from app.services import communication_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.core.vendor_scope import get_vendor_id_for_user
from app.models.user import User

router = APIRouter(prefix="/communications", tags=["Communication & Audit"])

def assert_can_access_message(db: Session, current_user: User, msg):
    vendor_id = get_vendor_id_for_user(db, current_user)
    if vendor_id is None:
        return

    if msg.vendor_id == vendor_id:
        return
    if current_user.id in (msg.sender_id, msg.receiver_id):
        return

    raise HTTPException(status_code=403, detail="You can only access your own messages")

def assert_can_access_file(db: Session, current_user: User, shared_file):
    vendor_id = get_vendor_id_for_user(db, current_user)
    if vendor_id is None:
        return
    if shared_file.vendor_id == vendor_id:
        return
    raise HTTPException(status_code=403, detail="You can only access your own shared files")

def enforce_sender_vendor(db: Session, current_user: User, data: CommunicationCreate):
    own_vendor_id = get_vendor_id_for_user(db, current_user)
    if own_vendor_id is None:
        return data
    if data.vendor_id and data.vendor_id != own_vendor_id:
        raise HTTPException(status_code=403, detail="You can only post messages on your own vendor record")
    data.vendor_id = own_vendor_id
    return data

@router.post("/messages", response_model=CommunicationResponse, status_code=201)
def send_message(
    data: CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = enforce_sender_vendor(db, current_user, data)
    return communication_service.send_message(db, data, current_user.id, current_user.name)

@router.post("/messages/upload", response_model=CommunicationResponse, status_code=201)
async def send_message_with_file(
    message: str = Form(...),
    vendor_id: Optional[int] = Form(None),
    procurement_id: Optional[int] = Form(None),
    po_id: Optional[int] = Form(None),
    contract_id: Optional[int] = Form(None),
    discussion_id: Optional[int] = Form(None),
    receiver_id: Optional[int] = Form(None),
    receiver_name: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = CommunicationCreate(
        vendor_id=vendor_id,
        procurement_id=procurement_id,
        po_id=po_id,
        contract_id=contract_id,
        discussion_id=discussion_id,
        receiver_id=receiver_id,
        receiver_name=receiver_name,
        message=message
    )
    data = enforce_sender_vendor(db, current_user, data)
    return communication_service.send_message(db, data, current_user.id, current_user.name, file=file)

@router.get("/messages", response_model=List[CommunicationResponse])
def get_conversations(
    vendor_id: Optional[int] = Query(None),
    po_id: Optional[int] = Query(None),
    contract_id: Optional[int] = Query(None),
    discussion_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    receiver_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    own_vendor_id = get_vendor_id_for_user(db, current_user)
    if own_vendor_id is not None:
        if vendor_id and vendor_id != own_vendor_id:
            raise HTTPException(status_code=403, detail="You can only read your own conversations")
        if not receiver_id:
            vendor_id = own_vendor_id

    if current_user.role == Roles.ADMIN:
        effective_user_id = user_id
    else:
        effective_user_id = current_user.id
    return communication_service.get_conversations(
        db,
        vendor_id=vendor_id,
        po_id=po_id,
        contract_id=contract_id,
        discussion_id=discussion_id,
        user_id=effective_user_id,
        receiver_id=receiver_id
    )

class MarkReadRequest(BaseModel):
    message_ids: Optional[List[int]] = None
    vendor_id: Optional[int] = None
    discussion_id: Optional[int] = None

@router.post("/messages/mark-read")
def mark_messages_read(
    body: Optional[MarkReadRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    body = body or MarkReadRequest()
    return communication_service.mark_messages_read(
        db,
        user_id=current_user.id,
        message_ids=body.message_ids,
        vendor_id=body.vendor_id,
        discussion_id=body.discussion_id,
        user_name=current_user.name
    )

@router.get("/messages/unread-count")
def unread_message_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor_id = None
    if current_user.role == Roles.VENDOR:
        from app.models.vendor import Vendor
        from sqlalchemy import func
        vendor = db.query(Vendor).filter(func.lower(Vendor.email) == current_user.email.lower()).first()
        vendor_id = vendor.id if vendor else None
    return {"unread_count": communication_service.get_unread_message_count(db, current_user.id, vendor_id)}

@router.post("/discussions", response_model=DiscussionResponse, status_code=201)
def create_discussion(
    data: DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_service.create_discussion(db, data, current_user.name, user_id=current_user.id)

@router.get("/discussions", response_model=List[DiscussionResponse])
def list_discussions(
    vendor_id: Optional[int] = Query(None),
    po_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    own_vendor_id = get_vendor_id_for_user(db, current_user)
    if own_vendor_id is not None:
        vendor_id = own_vendor_id
    return communication_service.get_discussions(db, vendor_id, po_id)


def _pending_communication_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_communication_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_communication_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_communication_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_communication_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_communication_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_communication_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_communication_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_communication_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows


def _pending_communication_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_communication_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "label", "")),
            "state": getattr(item, "status", "Unverified"),
            "updated": getattr(item, "updated_at", None),
        })
    return rows
