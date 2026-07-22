from fastapi import APIRouter, Depends, HTTPException, Query, Form, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse, VendorDocumentResponse
from app.services import vendor_service
from app.services import notification_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles, INTERNAL_ROLES
from app.models.user import User
from app.utils.uploads import (
    validate_upload,
    ALLOWED_DOCUMENT_EXTENSIONS,
    MAX_DOCUMENT_SIZE_BYTES,
)

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("/stats")
def vendor_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_vendor_stats(db)


@router.get("/recent", response_model=List[VendorResponse])
def recent_vendors(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_recent_vendors(db, limit)


@router.get("/me", response_model=VendorResponse)
def get_my_vendor_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.vendor import Vendor
    from sqlalchemy import func
    vendor = db.query(Vendor).filter(func.lower(Vendor.email) == current_user.email.lower()).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor profile not found for current user")
    return vendor


@router.get("/approved", response_model=List[VendorResponse])
def approved_vendors(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_assignable_vendors(db, category=category)


@router.post("/", response_model=VendorResponse, status_code=201)
def add_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    new_vendor = vendor_service.create_vendor(db, vendor, created_by=current_user.name)
    if not new_vendor:
        raise HTTPException(status_code=400, detail="Vendor with this email already exists")
    return new_vendor


@router.get("/", response_model=List[VendorResponse])
def view_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    category: Optional[str] = None,
    status: Optional[str] = None,
    approval_status: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_dir: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return vendor_service.get_all_vendors(
        db, skip=skip, limit=limit, category=category, status=status,
        approval_status=approval_status, keyword=keyword,
        sort_by=sort_by, sort_dir=sort_dir
    )


@router.get("/{vendor_id}", response_model=VendorResponse)
def view_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if current_user.role == Roles.VENDOR and vendor.email.lower() != current_user.email.lower():
        raise HTTPException(status_code=403, detail="You can only view your own vendor profile")
    return vendor


@router.put("/{vendor_id}", response_model=VendorResponse)
def modify_vendor(
    vendor_id: int, data: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    updated = vendor_service.update_vendor(db, vendor_id, data, updated_by=current_user.name)
    if not updated:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return updated


@router.delete("/{vendor_id}")
def remove_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    deleted = vendor_service.delete_vendor(db, vendor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deleted successfully"}


@router.post("/{vendor_id}/approve")
def approve(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    vendor = vendor_service.approve_vendor(db, vendor_id, current_user.name)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    notification_service.notify_vendor_approval_decision(db, vendor, approved=True)
    return {"message": "Vendor approved"}


@router.post("/{vendor_id}/reject")
def reject(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    vendor = vendor_service.reject_vendor(db, vendor_id, current_user.name)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    notification_service.notify_vendor_approval_decision(db, vendor, approved=False)
    return {"message": "Vendor rejected"}


@router.post("/{vendor_id}/block")
def block_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    vendor = vendor_service.block_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor blocked"}


@router.post("/{vendor_id}/deactivate")
def deactivate_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    vendor = vendor_service.deactivate_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor deactivated"}


@router.post("/{vendor_id}/activate")
def activate_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    vendor = vendor_service.activate_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found or not approved")
    return {"message": "Vendor activated"}


@router.post("/{vendor_id}/update-scores")
def update_scores(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.SUPPLY_CHAIN_MANAGER]))
):
    vendor = vendor_service.update_vendor_scores(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor scores updated", "reliability_score": vendor.reliability_score}


def _assert_can_read_vendor(db: Session, vendor_id: int, current_user: User):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if current_user.role == Roles.VENDOR and vendor.email.lower() != current_user.email.lower():
        raise HTTPException(status_code=403, detail="You can only access your own vendor documents")
    return vendor


@router.post("/{vendor_id}/documents", response_model=VendorDocumentResponse, status_code=201)
async def upload_vendor_document(
    vendor_id: int,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.vendor_document import VendorDocument
    import os

    _assert_can_read_vendor(db, vendor_id, current_user)

    document_type = (document_type or "").strip()
    if not document_type:
        raise HTTPException(status_code=400, detail="Document type is required")

    contents = validate_upload(file, ALLOWED_DOCUMENT_EXTENSIONS, MAX_DOCUMENT_SIZE_BYTES)

    upload_dir = os.path.join("static", "vendor_documents", str(vendor_id))
    os.makedirs(upload_dir, exist_ok=True)

    safe_filename = os.path.basename(file.filename)
    file_location = os.path.join(upload_dir, safe_filename)
    with open(file_location, "wb") as buffer:
        buffer.write(contents)

    doc = db.query(VendorDocument).filter(
        VendorDocument.vendor_id == vendor_id,
        VendorDocument.document_type == document_type
    ).first()

    if doc:
        previous_path = doc.file_path
        doc.file_name = safe_filename
        doc.file_path = file_location
        doc.uploaded_at = datetime.utcnow()
        if previous_path and os.path.normpath(previous_path) != os.path.normpath(file_location):
            try:
                os.remove(previous_path)
            except OSError:
                pass
    else:
        doc = VendorDocument(
            vendor_id=vendor_id,
            document_type=document_type,
            file_name=safe_filename,
            file_path=file_location
        )
        db.add(doc)

    db.commit()
    db.refresh(doc)
    return doc


@router.get("/{vendor_id}/documents", response_model=List[VendorDocumentResponse])
def get_vendor_documents(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.vendor_document import VendorDocument
    _assert_can_read_vendor(db, vendor_id, current_user)
    return db.query(VendorDocument).filter(
        VendorDocument.vendor_id == vendor_id
    ).order_by(VendorDocument.document_type.asc()).all()


@router.get("/{vendor_id}/documents/{document_id}/download")
def download_vendor_document(
    vendor_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.vendor_document import VendorDocument
    import os

    _assert_can_read_vendor(db, vendor_id, current_user)

    doc = db.query(VendorDocument).filter(
        VendorDocument.id == document_id,
        VendorDocument.vendor_id == vendor_id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="The stored file is no longer available on the server")

    return FileResponse(path=doc.file_path, filename=doc.file_name)


@router.delete("/{vendor_id}/documents/{document_id}")
def delete_vendor_document(
    vendor_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    from app.models.vendor_document import VendorDocument
    import os

    doc = db.query(VendorDocument).filter(
        VendorDocument.id == document_id,
        VendorDocument.vendor_id == vendor_id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    stored_path = doc.file_path
    db.delete(doc)
    db.commit()

    if stored_path:
        try:
            os.remove(stored_path)
        except OSError:
            pass

    return {"message": "Document deleted successfully"}
