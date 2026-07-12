from fastapi import HTTPException, status


class Roles:
    ADMIN = "Administrator"
    PROCUREMENT_MANAGER = "Procurement Manager"
    SUPPLY_CHAIN_MANAGER = "Supply Chain Manager"
    VENDOR = "Vendor"
    FINANCE_OFFICER = "Finance Officer"
    AUDITOR = "Auditor"


def admin_only(user):

    if user.role != Roles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator Access Required"
        )


def procurement_manager(user):

    if user.role not in [
        Roles.ADMIN,
        Roles.PROCUREMENT_MANAGER
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )


def supply_chain_manager(user):

    if user.role not in [
        Roles.ADMIN,
        Roles.SUPPLY_CHAIN_MANAGER
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )


def finance_officer(user):

    if user.role not in [
        Roles.ADMIN,
        Roles.FINANCE_OFFICER
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )


def auditor(user):

    if user.role not in [
        Roles.ADMIN,
        Roles.AUDITOR
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )


def vendor_only(user):

    if user.role != Roles.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor Access Only"
        )