from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.schemas.vendor_document import VendorDocumentCreate

from app.services.vendor_document_service import (
    upload_document,
    get_vendor_documents,
    get_document,
    delete_document
)

from app.core.dependencies import get_current_user
from app.core.roles import (
    procurement_manager,
    admin_only
)

router = APIRouter()


# =====================================
# Upload Vendor Document
# =====================================
@router.post("/vendors/{vendor_id}/documents")
def upload_vendor_document(
    vendor_id: int,
    document: VendorDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    new_document = upload_document(
        db,
        vendor_id,
        document
    )

    if new_document is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return {
        "message": "Document Uploaded Successfully",
        "document": new_document
    }


# =====================================
# Get Vendor Documents
# =====================================
@router.get("/vendors/{vendor_id}/documents")
def read_vendor_documents(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_vendor_documents(
        db,
        vendor_id
    )


# =====================================
# Get Single Document
# =====================================
@router.get("/documents/{document_id}")
def read_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    document = get_document(
        db,
        document_id
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document Not Found"
        )

    return document


# =====================================
# Delete Document
# =====================================
@router.delete("/documents/{document_id}")
def remove_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    admin_only(current_user)

    deleted = delete_document(
        db,
        document_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Document Not Found"
        )

    return {
        "message": "Document Deleted Successfully"
    }