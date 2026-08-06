from fastapi import APIRouter, Depends, HTTPException, Query, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse, VendorDocumentResponse
from app.services import vendor_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("/stats")
def vendor_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return KPI counts for the dashboard (total, approved, pending, high risk, etc.)"""
    return vendor_service.get_vendor_stats(db)


@router.get("/recent", response_model=List[VendorResponse])
def recent_vendors(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return the most recently added vendors for the dashboard table."""
    return vendor_service.get_recent_vendors(db, limit)




@router.post("/", response_model=VendorResponse, status_code=201)
def add_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    new_vendor = vendor_service.create_vendor(db, vendor)
    if not new_vendor:
        raise HTTPException(status_code=400, detail="Vendor with this email already exists")
    return new_vendor


@router.get("/", response_model=List[VendorResponse])
def view_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return vendor_service.get_all_vendors(db, skip=skip, limit=limit,
                                          category=category, status=status)


@router.get("/{vendor_id}", response_model=VendorResponse)
def view_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.put("/{vendor_id}", response_model=VendorResponse)
def modify_vendor(
    vendor_id: int, data: VendorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    updated = vendor_service.update_vendor(db, vendor_id, data)
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
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    vendor = vendor_service.approve_vendor(db, vendor_id, current_user.name)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"message": "Vendor approved"}


@router.post("/{vendor_id}/reject")
def reject(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN]))
):
    vendor = vendor_service.reject_vendor(db, vendor_id, current_user.name)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
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
    import shutil

    vendor = vendor_service.get_vendor(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    upload_dir = os.path.join("static", "vendor_documents", str(vendor_id))
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = VendorDocument(
        vendor_id=vendor_id,
        document_type=document_type,
        file_name=file.filename,
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
    return db.query(VendorDocument).filter(VendorDocument.vendor_id == vendor_id).all()


@router.delete("/{vendor_id}/documents/{document_id}")
def delete_vendor_document(
    vendor_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER]))
):
    from app.models.vendor_document import VendorDocument
    doc = db.query(VendorDocument).filter(
        VendorDocument.id == document_id,
        VendorDocument.vendor_id == vendor_id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}
