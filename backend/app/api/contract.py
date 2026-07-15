from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractCreate

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.get("/")
def get_contracts(db: Session = Depends(get_db)):
    return db.query(Contract).all()

@router.post("/")
def create_contract(data: ContractCreate, db: Session = Depends(get_db)):
    contract = Contract(**data.dict())
    db.add(contract)
    db.commit()
    return contract
