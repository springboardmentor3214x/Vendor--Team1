from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.vendor_document import VendorDocument
from app.schemas.vendor_document import VendorDocumentCreate


def upload_document(
    db: Session,
    vendor_id: int,
    document: VendorDocumentCreate
):
    vendor = db.query(Vendor).filter(
        Vendor.id == vendor_id
    ).first()

    if vendor is None:
        return None

    new_document = VendorDocument(
        vendor_id=vendor_id,
        document_name=document.document_name,
        document_type=document.document_type,
        file_path=document.file_path
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


def get_vendor_documents(
    db: Session,
    vendor_id: int
):
    return db.query(VendorDocument).filter(
        VendorDocument.vendor_id == vendor_id
    ).all()


def get_document(
    db: Session,
    document_id: int
):
    return db.query(VendorDocument).filter(
        VendorDocument.id == document_id
    ).first()


def delete_document(
    db: Session,
    document_id: int
):
    document = db.query(VendorDocument).filter(
        VendorDocument.id == document_id
    ).first()

    if document is None:
        return None

    db.delete(document)
    db.commit()

    return document