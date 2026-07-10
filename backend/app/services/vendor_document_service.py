import os
import shutil

from fastapi import UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.vendor_document import VendorDocument

UPLOAD_FOLDER = "uploads"


# --------------------------------------------------
# Upload Document
# --------------------------------------------------

def upload_document(
    db: Session,
    vendor_id: int,
    document_type: str,
    file: UploadFile = File(...)
):

    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_location = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    new_document = VendorDocument(
        vendor_id=vendor_id,
        document_type=document_type,
        file_name=file.filename,
        file_path=file_location
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Document Uploaded Successfully",
        "document": new_document
    }


# --------------------------------------------------
# Get All Documents
# --------------------------------------------------

def get_all_documents(db: Session):

    return db.query(VendorDocument).all()


# --------------------------------------------------
# Get One Document
# --------------------------------------------------

def get_document(
    db: Session,
    document_id: int
):

    return db.query(VendorDocument).filter(
        VendorDocument.id == document_id
    ).first()


# --------------------------------------------------
# Delete Document
# --------------------------------------------------

def delete_document(
    db: Session,
    document_id: int
):

    document = db.query(VendorDocument).filter(
        VendorDocument.id == document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document Not Found"
        )

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return {
        "message": "Document Deleted Successfully"
    }