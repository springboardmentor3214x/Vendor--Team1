from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.services.vendor_document_service import (
    upload_document,
    get_all_documents,
    get_document,
    delete_document
)

router = APIRouter(
    prefix="/vendor-documents",
    tags=["Vendor Documents"]
)


# --------------------------------------------------
# Upload Document
# --------------------------------------------------

@router.post("/upload")
def upload_vendor_document(

    vendor_id: int = Form(...),

    document_type: str = Form(...),

    file: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    return upload_document(

        db,

        vendor_id,

        document_type,

        file

    )


# --------------------------------------------------
# Get All Documents
# --------------------------------------------------

@router.get("/")
def read_all_documents(

    db: Session = Depends(get_db)

):

    return get_all_documents(db)


# --------------------------------------------------
# Get One Document
# --------------------------------------------------

@router.get("/{document_id}")
def read_document(

    document_id: int,

    db: Session = Depends(get_db)

):

    return get_document(

        db,

        document_id

    )


# --------------------------------------------------
# Delete Document
# --------------------------------------------------

@router.delete("/{document_id}")
def remove_document(

    document_id: int,

    db: Session = Depends(get_db)

):

    return delete_document(

        db,

        document_id

    )