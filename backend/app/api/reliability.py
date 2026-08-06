from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.services import reliability_service
from app.core.dependencies import get_current_user, role_required
from app.core.roles import Roles
from app.models.user import User

router = APIRouter(prefix="/reliability", tags=["Vendor Reliability"])


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reliability_service.get_reliability_dashboard(db)


@router.get("/details/{vendor_id}")
def get_details(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    details = reliability_service.get_vendor_reliability_details(db, vendor_id)
    if not details:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return details


@router.get("/rankings")
def get_rankings(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reliability_service.get_supplier_rankings(db, category=category)


@router.get("/risk-assessment")
def get_risk_assessment(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER, Roles.AUDITOR]))
):
    return reliability_service.get_procurement_risk_assessment(db)


@router.get("/trends/{vendor_id}")
def get_trends(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trends = reliability_service.get_performance_trends(db, vendor_id)
    if not trends:
        raise HTTPException(status_code=404, detail="Vendor trends not found")
    return trends


@router.get("/recommendations")
def get_recommendations(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required([Roles.ADMIN, Roles.PROCUREMENT_MANAGER, Roles.SUPPLY_CHAIN_MANAGER]))
):
    return reliability_service.get_procurement_recommendations(db, category=category)
