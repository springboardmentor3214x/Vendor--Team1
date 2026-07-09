from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.contract import ContractCreate

from app.services.contract_service import (

    create_contract,

    get_all_contracts,

    get_contract,

    update_contract,

    delete_contract

)

router = APIRouter()


@router.post("/contracts")
def add_contract(

    contract: ContractCreate,

    db: Session = Depends(get_db)

):

    return create_contract(db, contract)


@router.get("/contracts")
def all_contracts(

    db: Session = Depends(get_db)

):

    return get_all_contracts(db)


@router.get("/contracts/{contract_id}")
def one_contract(

    contract_id: int,

    db: Session = Depends(get_db)

):

    contract = get_contract(db, contract_id)

    if contract is None:

        raise HTTPException(

            status_code=404,

            detail="Contract Not Found"

        )

    return contract


@router.put("/contracts/{contract_id}")
def edit_contract(

    contract_id: int,

    contract: ContractCreate,

    db: Session = Depends(get_db)

):

    updated = update_contract(

        db,

        contract_id,

        contract

    )

    if updated is None:

        raise HTTPException(

            status_code=404,

            detail="Contract Not Found"

        )

    return updated


@router.delete("/contracts/{contract_id}")
def remove_contract(

    contract_id: int,

    db: Session = Depends(get_db)

):

    deleted = delete_contract(

        db,

        contract_id

    )

    if deleted is None:

        raise HTTPException(

            status_code=404,

            detail="Contract Not Found"

        )

    return {

        "message": "Contract Deleted Successfully"

    }