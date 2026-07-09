from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.services.analytics_service import (dashboard_summary, vendor_analytics)

router = APIRouter()


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db)
):

    return dashboard_summary(db)
@router.get("/analytics/vendors")
def get_vendor_analytics(

    db: Session = Depends(get_db)

):

    return vendor_analytics(db)