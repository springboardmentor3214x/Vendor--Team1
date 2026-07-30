from app.database.connection import engine, SessionLocal
from app.database.base import Base
from app.core.security import hash_password
from app.core.roles import Roles
from app.models.user import User
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.procurement_status_history import ProcurementStatusHistory
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.models.contract import Contract
from app.models.communication import Communication
from app.models.purchase_order import PurchaseOrder
from app.models.order_tracking import OrderTracking
from app.models.invoice import Invoice
from app.models.vendor_document import VendorDocument
from app.models.certification import Certification
from app.models.compliance_record import ComplianceRecord
from app.models.discussion import Discussion
from app.models.notification import Notification
from app.models.activity_log import ActivityLog
from app.models.shared_file import SharedFile
from datetime import datetime, timedelta, date
from app.utils.delivery_timing import delivery_status_from_times

SHIPPING_ADDRESS = "Corporate Office, Cyber City, Gurgaon, Haryana 122002"

GST_RATE = 0.18

def _delivery_row(vendor_id, procurement_id, expected, actual, remarks):
    status, delay_hours, delay_days = delivery_status_from_times(expected, actual)
    return DeliveryPerformance(
        vendor_id=vendor_id,
        procurement_id=procurement_id,
        expected_date=expected,
        actual_date=actual,
        delay_days=delay_days,
        delay_hours=delay_hours,
        delivery_status=status,
        remarks=remarks,
    )

DEFAULT_USERS = [
    {
        "name": "Admin User",
        "email": "admin@vendor.com",
        "mobile_number": "9876543210",
        "password": "Admin@123",
        "role": Roles.ADMIN,
    },
    {
        "name": "Procurement Manager",
        "email": "procurement@vendor.com",
        "mobile_number": "9876543211",
        "password": "Procure@123",
        "role": Roles.PROCUREMENT_MANAGER,
    },
    {
        "name": "Supply Chain Manager",
        "email": "supplychain@vendor.com",
        "mobile_number": "9876543212",
        "password": "Supply@123",
        "role": Roles.SUPPLY_CHAIN_MANAGER,
    },
    {
        "name": "Vendor User",
        "email": "vendor@vendor.com",
        "mobile_number": "9876543213",
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    },
    {
        "name": "Finance Manager",
        "email": "finance@vendor.com",
        "mobile_number": "9876543214",
        "password": "Finance@123",
        "role": Roles.FINANCE_OFFICER,
    },
    {
        "name": "Auditor User",
        "email": "auditor@vendor.com",
        "mobile_number": "9876543215",
        "password": "Auditor@123",
        "role": Roles.AUDITOR,
    },
    {
        "name": "Rajesh Kumar",
        "email": "rajesh@techsupply.in",
        "mobile_number": "9112345678",
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    },
    {
        "name": "Priya Sharma",
        "email": "priya@officemart.co.in",
        "mobile_number": "9223456789",
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    },
    {
        "name": "Amit Patel",
        "email": "amit@cloudinfra.io",
        "mobile_number": "9334567890",
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    },
    {
        "name": "Suresh Reddy",
        "email": "suresh@buildright.in",
        "mobile_number": "9445678901",
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    },
    {
        "name": "Kavitha Nair",
        "email": "kavitha@greenpack.in",
        "mobile_number": "9556789012",
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    },
]


def _pending_seed_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_seed_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_seed_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_seed_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_seed_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_seed_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_seed_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_seed_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_seed_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_seed_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_seed_rows_6(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_seed_totals_6(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
