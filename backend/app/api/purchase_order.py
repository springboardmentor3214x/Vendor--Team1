from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.purchase_order import PurchaseOrderCreate

from app.services.purchase_order_service import (

    create_purchase_order,

    get_all_purchase_orders,

    get_purchase_order,

    update_purchase_order,

    delete_purchase_order

)

router = APIRouter()


@router.post("/purchase-orders")
def add_purchase_order(

    purchase: PurchaseOrderCreate,

    db: Session = Depends(get_db)

):

    return create_purchase_order(db, purchase)


@router.get("/purchase-orders")
def all_purchase_orders(

    db: Session = Depends(get_db)

):

    return get_all_purchase_orders(db)


@router.get("/purchase-orders/{purchase_id}")
def one_purchase_order(

    purchase_id: int,

    db: Session = Depends(get_db)

):

    purchase = get_purchase_order(db, purchase_id)

    if purchase is None:

        raise HTTPException(

            status_code=404,

            detail="Purchase Order Not Found"

        )

    return purchase


@router.put("/purchase-orders/{purchase_id}")
def edit_purchase_order(

    purchase_id: int,

    purchase: PurchaseOrderCreate,

    db: Session = Depends(get_db)

):

    updated = update_purchase_order(

        db,

        purchase_id,

        purchase

    )

    if updated is None:

        raise HTTPException(

            status_code=404,

            detail="Purchase Order Not Found"

        )

    return updated


@router.delete("/purchase-orders/{purchase_id}")
def remove_purchase_order(

    purchase_id: int,

    db: Session = Depends(get_db)

):

    deleted = delete_purchase_order(

        db,

        purchase_id

    )

    if deleted is None:

        raise HTTPException(

            status_code=404,

            detail="Purchase Order Not Found"

        )

    return {

        "message": "Purchase Order Deleted Successfully"

    }