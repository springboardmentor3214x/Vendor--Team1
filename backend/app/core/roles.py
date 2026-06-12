class Roles:
    ADMIN = "Administrator"
    PROCUREMENT_MANAGER = "Procurement Manager"
    SUPPLY_CHAIN_MANAGER = "Supply Chain Manager"
    VENDOR = "Vendor"
    FINANCE_OFFICER = "Finance Officer"
    AUDITOR = "Auditor"


ALL_ROLES = [
    Roles.ADMIN, Roles.PROCUREMENT_MANAGER,
    Roles.SUPPLY_CHAIN_MANAGER, Roles.VENDOR,
    Roles.FINANCE_OFFICER, Roles.AUDITOR
]

INTERNAL_ROLES = [r for r in ALL_ROLES if r != Roles.VENDOR]

VENDOR_MANAGER_ROLES = [Roles.ADMIN, Roles.PROCUREMENT_MANAGER]
