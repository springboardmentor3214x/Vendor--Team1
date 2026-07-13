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


def _pending_communication_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
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
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
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
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
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
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
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
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
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
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_communication_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
