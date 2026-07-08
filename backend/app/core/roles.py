from fastapi import HTTPException


def admin_only(user):

    if user.role != "Administrator":
        raise HTTPException(
            status_code=403,
            detail="Administrator Access Required"
        )


def procurement_manager(user):

    if user.role not in [
        "Administrator",
        "Procurement Manager"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )


def supply_chain_manager(user):

    if user.role not in [
        "Administrator",
        "Supply Chain Manager"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )