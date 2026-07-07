from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.vendor_performance import VendorPerformanceCreate
from app.services.vendor_performance_service import create_performance

router = APIRouter()


@router.post("/performance")
def add_performance(
    performance: VendorPerformanceCreate,
    db: Session = Depends(get_db)
):
    return create_performance(db, performance)