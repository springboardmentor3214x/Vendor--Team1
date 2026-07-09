from sqlalchemy.orm import Session

from app.models.contract import Contract
from app.schemas.contract import ContractCreate


def create_contract(db: Session, contract: ContractCreate):

    new_contract = Contract(

        purchase_order_id=contract.purchase_order_id,

        contract_number=contract.contract_number,

        contract_title=contract.contract_title,

        start_date=contract.start_date,

        end_date=contract.end_date,

        contract_value=contract.contract_value,

        status=contract.status,

        terms_conditions=contract.terms_conditions

    )

    db.add(new_contract)

    db.commit()

    db.refresh(new_contract)

    return new_contract


def get_all_contracts(db: Session):

    return db.query(Contract).all()


def get_contract(db: Session, contract_id: int):

    return db.query(Contract).filter(

        Contract.id == contract_id

    ).first()


def update_contract(

    db: Session,

    contract_id: int,

    contract: ContractCreate

):

    existing = db.query(Contract).filter(

        Contract.id == contract_id

    ).first()

    if existing is None:

        return None

    existing.purchase_order_id = contract.purchase_order_id

    existing.contract_number = contract.contract_number

    existing.contract_title = contract.contract_title

    existing.start_date = contract.start_date

    existing.end_date = contract.end_date

    existing.contract_value = contract.contract_value

    existing.status = contract.status

    existing.terms_conditions = contract.terms_conditions

    db.commit()

    db.refresh(existing)

    return existing


def delete_contract(

    db: Session,

    contract_id: int

):

    contract = db.query(Contract).filter(

        Contract.id == contract_id

    ).first()

    if contract is None:

        return None

    db.delete(contract)

    db.commit()

    return contract