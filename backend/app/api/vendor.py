from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.vendor import VendorCreate, VendorScoreUpdate
from app.models.user import User

from app.services.vendor_service import (
    create_vendor,
    get_all_vendors,
    get_vendor,
    update_vendor,
    delete_vendor,
    approve_vendor,
    reject_vendor,
    search_vendors,
    filter_vendors_by_status,
    filter_vendors_by_category,
    vendor_dashboard,
    get_vendors_paginated,
    sort_vendors,
    calculate_reliability_score,
    top_vendors,
    bottom_vendors,
    vendor_performance_report,
    update_vendor_scores
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
# Search Vendors
# Any Logged-in User
# =====================================
@router.get("/vendors/search")
def search_vendor(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    vendors = search_vendors(
        db,
        keyword
    )

    return vendors
# =====================================
# Filter Vendors By Status
# Any Logged-in User
# =====================================
@router.get("/vendors/filter/status")
def filter_vendor_status(
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return filter_vendors_by_status(
        db,
        status
    )
# =====================================
# Filter Vendors By Category
# Any Logged-in User
# =====================================
@router.get("/vendors/filter/category")
def filter_vendor_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return filter_vendors_by_category(
        db,
        category
    )
# =====================================
# Vendor Dashboard
# Administrator & Procurement Manager
# =====================================
@router.get("/vendors/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    return vendor_dashboard(db)
# =====================================
# Vendor Pagination
# Any Logged-in User
# =====================================
@router.get("/vendors/page")
def vendor_pagination(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_vendors_paginated(
        db,
        page,
        limit
    )
# =====================================
# Sort Vendors
# Any Logged-in User
# =====================================
@router.get("/vendors/sort")
def vendor_sort(
    field: str,
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return sort_vendors(
        db,
        field,
        order
    )
    
# =====================================
# Top Vendors
# Any Logged-in User
# =====================================
@router.get("/vendors/top")
def get_top_vendors(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return top_vendors(
        db,
        limit
    )
    
# =====================================
# Bottom Vendors
# Any Logged-in User
# =====================================
@router.get("/vendors/bottom")
def get_bottom_vendors(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return bottom_vendors(
        db,
        limit
    )
    
# =====================================
# Vendor Performance Report
# Any Logged-in User
# =====================================
@router.get("/vendors/{vendor_id}/performance")
def performance_report(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    report = vendor_performance_report(
        db,
        vendor_id
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return report

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
# Calculate Vendor Reliability Score
# Administrator & Procurement Manager
# =====================================
@router.post("/vendors/{vendor_id}/calculate-score")
def calculate_vendor_score(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    vendor = calculate_reliability_score(
        db,
        vendor_id
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return {
        "message": "Vendor Reliability Score Calculated Successfully",
        "vendor_name": vendor.vendor_name,
        "reliability_score": vendor.reliability_score
    }


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
# =====================================
# Approve Vendor
# Administrator & Procurement Manager
# =====================================
@router.post("/vendors/{vendor_id}/approve")
def approve_vendor_api(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    vendor = approve_vendor(
        db,
        vendor_id,
        current_user.name
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return {
        "message": "Vendor Approved Successfully",
        "vendor": vendor
    }


# =====================================
# Reject Vendor
# Administrator & Procurement Manager
# =====================================
@router.post("/vendors/{vendor_id}/reject")
def reject_vendor_api(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    vendor = reject_vendor(
        db,
        vendor_id,
        current_user.name
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return {
        "message": "Vendor Rejected Successfully",
        "vendor": vendor
    }
@router.put("/vendors/{vendor_id}/scores")
def update_scores(
    vendor_id: int,
    scores: VendorScoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    vendor = update_vendor_scores(
        db,
        vendor_id,
        scores
    )

    if vendor is None:
        raise HTTPException(
            status_code=404,
            detail="Vendor Not Found"
        )

    return {
        "message": "Vendor Scores Updated Successfully",
        "vendor": vendor
    }