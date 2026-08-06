from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.communication import CommunicationCreate, CommunicationResponse
from app.schemas.discussion import DiscussionCreate, DiscussionResponse
from app.schemas.shared_file import SharedFileResponse
from app.schemas.activity_log import ActivityLogResponse
from app.services import communication_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/communication", tags=["Communication & Audit"])


@router.post("/messages", response_model=CommunicationResponse, status_code=201)
def send_message(
    data: CommunicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
    return communication_service.send_message(db, data, current_user.id, current_user.name, file=file)


@router.get("/messages", response_model=List[CommunicationResponse])
def get_conversations(
    vendor_id: Optional[int] = Query(None),
    po_id: Optional[int] = Query(None),
    contract_id: Optional[int] = Query(None),
    discussion_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_service.get_conversations(db, vendor_id, po_id, contract_id, discussion_id)


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
    return communication_service.get_discussions(db, vendor_id, po_id)


@router.post("/files/upload", response_model=SharedFileResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    vendor_id: Optional[int] = Form(None),
    procurement_id: Optional[int] = Form(None),
    po_id: Optional[int] = Form(None),
    contract_id: Optional[int] = Form(None),
    discussion_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_service.upload_shared_file(
        db, current_user.name, file, vendor_id, procurement_id, po_id, contract_id, discussion_id
    )


@router.get("/files", response_model=List[SharedFileResponse])
def list_files(
    vendor_id: Optional[int] = Query(None),
    po_id: Optional[int] = Query(None),
    contract_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_service.get_shared_files(db, vendor_id, po_id, contract_id)


@router.get("/activity-logs", response_model=List[ActivityLogResponse])
def list_activity_logs(
    module: Optional[str] = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return communication_service.get_activity_logs(db, limit=limit, module_name=module)
