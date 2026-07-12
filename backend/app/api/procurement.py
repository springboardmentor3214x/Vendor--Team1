from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User

from app.schemas.procurement import ProcurementCreate

from app.services.procurement_service import (
    create_procurement,
    get_all_procurements,
    get_procurement,
    update_procurement,
    delete_procurement,
    approve_procurement,
    reject_procurement,
    search_procurements
)

from app.core.dependencies import get_current_user
from app.core.roles import (
    procurement_manager,
    admin_only
)

router = APIRouter()


# =====================================
# Create Procurement
# =====================================
@router.post("/procurements")
def add_procurement(
    procurement: ProcurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    return create_procurement(
        db,
        procurement
    )


# =====================================
# Get All Procurements
# =====================================
@router.get("/procurements")
def all_procurements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_all_procurements(db)

# =====================================
# Search Procurement
# =====================================
@router.get("/procurements/search")
def search_procurement_api(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return search_procurements(
        db,
        keyword
    )


# =====================================
# Get Procurement By ID
# =====================================
@router.get("/procurements/{procurement_id}")
def one_procurement(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement = get_procurement(
        db,
        procurement_id
    )

    if procurement is None:
        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return procurement


# =====================================
# Update Procurement
# =====================================
@router.put("/procurements/{procurement_id}")
def edit_procurement(
    procurement_id: int,
    procurement: ProcurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    updated = update_procurement(
        db,
        procurement_id,
        procurement
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return updated


# =====================================
# Delete Procurement
# =====================================
@router.delete("/procurements/{procurement_id}")
def remove_procurement(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    admin_only(current_user)

    deleted = delete_procurement(
        db,
        procurement_id
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return {
        "message": "Procurement Deleted Successfully"
    }
# =====================================
# Approve Procurement
# =====================================
@router.post("/procurements/{procurement_id}/approve")
def approve_procurement_api(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    procurement = approve_procurement(
        db,
        procurement_id,
        current_user.name
    )

    if procurement is None:
        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return {
        "message": "Procurement Approved Successfully",
        "procurement": procurement
    }


# =====================================
# Reject Procurement
# =====================================
@router.post("/procurements/{procurement_id}/reject")
def reject_procurement_api(
    procurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    procurement_manager(current_user)

    procurement = reject_procurement(
        db,
        procurement_id,
        current_user.name
    )

    if procurement is None:
        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return {
        "message": "Procurement Rejected Successfully",
        "procurement": procurement
    }
