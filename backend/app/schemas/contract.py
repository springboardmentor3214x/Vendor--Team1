from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class ContractCreate(BaseModel):
    contract_title: str
    vendor_id: int
    vendor_name: Optional[str] = None
    contract_type: Optional[str] = "Master Agreement"
    procurement_category: Optional[str] = None
    start_date: date
    end_date: date
    contract_value: float

class ContractUpdate(BaseModel):
    contract_title: Optional[str] = None
    contract_type: Optional[str] = None
    procurement_category: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    contract_value: Optional[float] = None
    payment_terms: Optional[str] = None


def _pending_contract_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_contract_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
