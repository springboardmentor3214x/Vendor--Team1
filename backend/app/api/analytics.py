from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services import analytics_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Dashboard & Analytics"])


@router.get("/procurement-manager-dashboard")
def get_procurement_manager_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER]))
):
    return analytics_service.get_procurement_manager_dashboard_analytics(db)


@router.get("/vendor-dashboard/{vendor_id}")
def get_vendor_dashboard(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify vendor role permissions if current user is vendor
    if current_user.role == Roles.VENDOR:
        # Check if user matches vendor email
        from app.models.vendor import Vendor
        v = db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if not v or v.email.lower() != current_user.email.lower():
            raise HTTPException(status_code=403, detail="Not authorized to access another vendor's dashboard")

    analytics = analytics_service.get_vendor_dashboard_analytics(db, vendor_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Vendor analytics not found")
    return analytics


@router.get("/admin-dashboard")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.AUDITOR]))
):
    return analytics_service.get_admin_dashboard_analytics(db)
