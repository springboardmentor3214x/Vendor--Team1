from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.vendor import VendorCreate
from app.models.user import User

from app.services.vendor_service import (
    create_vendor,
    get_all_vendors,
    get_vendor,
    update_vendor,
    delete_vendor
)

from app.core.dependencies import get_current_user
from app.core.roles import (
    admin_only,
    procurement_manager
)

router = APIRouter()


# =====================================
# Add Vendor
# Administrator & Procurement Manager
# =====================================
@router.post("/vendors")
def add_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    return create_vendor(db, vendor)


# =====================================
# Get All Vendors
# Any Logged-in User
# =====================================
@router.get("/vendors")
def all_vendors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_all_vendors(db)


# =====================================
# Get Vendor By ID
# Any Logged-in User
# =====================================
@router.get("/vendors/{vendor_id}")
def one_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    vendor = get_vendor(db, vendor_id)

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return vendor


# =====================================
# Update Vendor
# Administrator & Procurement Manager
# =====================================
@router.put("/vendors/{vendor_id}")
def edit_vendor(
    vendor_id: int,
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    updated = update_vendor(
        db,
        vendor_id,
        vendor
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return updated


# =====================================
# Delete Vendor
# Administrator Only
# =====================================
@router.delete("/vendors/{vendor_id}")
def remove_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    admin_only(current_user)

    deleted = delete_vendor(
        db,
        vendor_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return {
        "message": "Vendor Deleted Successfully"
    }