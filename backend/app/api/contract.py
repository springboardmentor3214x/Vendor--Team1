from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.contract import Contract
from app.models.vendor import Vendor
from app.schemas.contract import ContractCreate, ContractResponse

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.get("/")
def get_contracts(db: Session = Depends(get_db)):
    return db.query(Contract).all()

@router.post("/")
def create_contract(data: ContractCreate, db: Session = Depends(get_db)):
    # Auto-resolve vendor name if not provided
    vendor_name = data.vendor_name
    if not vendor_name:
        vendor = db.query(Vendor).filter(Vendor.id == data.vendor_id).first()
        if vendor:
            vendor_name = vendor.company_name
        else:
            vendor_name = "Unknown Vendor"

    contract_data = data.dict()
    contract_data["vendor_name"] = vendor_name

    contract = Contract(**contract_data)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract
