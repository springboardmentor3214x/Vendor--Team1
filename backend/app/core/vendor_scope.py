from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.roles import Roles
from app.models.user import User


def get_vendor_id_for_user(db: Session, user: User) -> Optional[int]:
    if user.role != Roles.VENDOR:
        return None

    from app.models.vendor import Vendor

    vendor = db.query(Vendor).filter(func.lower(Vendor.email) == user.email.lower()).first()
    return vendor.id if vendor else -1


def assert_owns(db: Session, user: User, record_vendor_id: Optional[int], noun: str = "record"):
    scope = get_vendor_id_for_user(db, user)
    if scope is not None and record_vendor_id != scope:
        raise HTTPException(
            status_code=403,
            detail=f"You can only access your own {noun}"
        )


def restrict_to_vendor(db: Session, user: User, records: list, noun: str = "records") -> list:
    scope = get_vendor_id_for_user(db, user)
    if scope is None:
        return records
    return [r for r in records if getattr(r, "vendor_id", None) == scope]
