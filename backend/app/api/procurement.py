from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.procurement import ProcurementCreate

from app.services.procurement_service import (

    create_procurement,

    get_all_procurements,

    get_procurement,

    update_procurement,

    delete_procurement

)

router = APIRouter()


@router.post("/procurements")
def add_procurement(
    procurement: ProcurementCreate,
    db: Session = Depends(get_db)
):

    return create_procurement(db, procurement)


@router.get("/procurements")
def all_procurements(
    db: Session = Depends(get_db)
):

    return get_all_procurements(db)


@router.get("/procurements/{procurement_id}")
def one_procurement(
    procurement_id: int,
    db: Session = Depends(get_db)
):

    procurement = get_procurement(db, procurement_id)

    if procurement is None:

        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return procurement


@router.put("/procurements/{procurement_id}")
def edit_procurement(
    procurement_id: int,
    procurement: ProcurementCreate,
    db: Session = Depends(get_db)
):

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


@router.delete("/procurements/{procurement_id}")
def remove_procurement(
    procurement_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_procurement(db, procurement_id)

    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="Procurement Not Found"
        )

    return {

        "message": "Procurement Deleted Successfully"

    }