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

DEFAULT_VENDORS = [
    {
        "vendor_name": "Vendor User",
        "company_name": "Global Vendor Solutions",
        "email": "vendor@vendor.com",
        "phone": "9876543213",
        "address": "Tower B, Cyber City, Gurgaon, Haryana 122002",
        "category": "IT Vendors",
        "contact_person": "Vendor User",
        "designation": "Managing Director",
        "alternate_phone": "9876500213",
        "gst_number": "06AABCG1234H1Z2",
        "pan_number": "AABCG1234H",
        "company_registration_number": "U72200HR2018PTC074512",
        "address_line_1": "Tower B, 4th Floor, DLF Cyber City",
        "address_line_2": "Phase III, Sector 24",
        "city": "Gurgaon",
        "state": "Haryana",
        "country": "India",
        "pincode": "122002",
        "website": "https://www.globalvendorsolutions.in",
        "description": (
            "Full-service IT procurement partner supplying enterprise hardware, licensing and "
            "managed support across North India. Operates an ISO-certified logistics hub in Gurgaon."
        ),
        "bank_account_number": "501000234567891",
        "ifsc_code": "HDFC0001234",
        "payment_terms": "Net 30",
        "delivery_score": 88.0,
        "quality_score": 92.0,
        "communication_score": 85.0,
        "service_score": 90.0,
        "reliability_score": 88.7,
        "status": "Active",
        "approval_status": "Approved",
        "approved_by": "Admin User",
    },
    {
        "vendor_name": "Rajesh Kumar",
        "company_name": "TechSupply India Pvt Ltd",
        "email": "rajesh@techsupply.in",
        "phone": "9112345678",
        "address": "Plot 44, Sector 62, Noida, Uttar Pradesh 201309",
        "category": "IT Vendors",
        "contact_person": "Rajesh Kumar",
        "designation": "Chief Executive Officer",
        "alternate_phone": "9112300678",
        "gst_number": "09AABCT1234F1Z5",
        "pan_number": "AABCT1234F",
        "company_registration_number": "U30007UP2016PTC085431",
        "address_line_1": "Plot 44, Ground & First Floor",
        "address_line_2": "Sector 62, Institutional Area",
        "city": "Noida",
        "state": "Uttar Pradesh",
        "country": "India",
        "pincode": "201309",
        "website": "https://www.techsupplyindia.in",
        "description": (
            "Authorised reseller for Dell, Cisco and Lenovo enterprise hardware. Supplies laptops, "
            "networking equipment and server infrastructure with on-site warranty support."
        ),
        "bank_account_number": "912010045678123",
        "ifsc_code": "ICIC0000456",
        "payment_terms": "Net 45",
        "delivery_score": 84.0,
        "quality_score": 90.0,
        "communication_score": 80.0,
        "service_score": 86.0,
        "reliability_score": 85.0,
        "status": "Active",
        "approval_status": "Approved",
        "approved_by": "Admin User",
    },
    {
        "vendor_name": "Priya Sharma",
        "company_name": "OfficeMart Solutions",
        "email": "priya@officemart.co.in",
        "phone": "9223456789",
        "address": "128, MG Road, Bangalore, Karnataka 560001",
        "category": "Service Providers",
        "contact_person": "Priya Sharma",
        "designation": "Operations Head",
        "alternate_phone": "9223400789",
        "gst_number": "29AACCO5678K1Z9",
        "pan_number": "AACCO5678K",
        "company_registration_number": "U51909KA2015PTC079842",
        "address_line_1": "128, Prestige Meridian, MG Road",
        "address_line_2": "Near Trinity Metro Station",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "pincode": "560001",
        "website": "https://www.officemartsolutions.co.in",
        "description": (
            "Corporate office supplies and furniture provider serving 200+ enterprise clients in "
            "South India. Offers ergonomic workstation design and installation services."
        ),
        "bank_account_number": "3456789012345",
        "ifsc_code": "SBIN0004567",
        "payment_terms": "Net 30",
        "delivery_score": 76.0,
        "quality_score": 80.0,
        "communication_score": 84.0,
        "service_score": 78.0,
        "reliability_score": 79.4,
        "status": "Active",
        "approval_status": "Approved",
        "approved_by": "Admin User",
    },
    {
        "vendor_name": "Amit Patel",
        "company_name": "CloudInfra Services",
        "email": "amit@cloudinfra.io",
        "phone": "9334567890",
        "address": "Cyber Towers, HITEC City, Hyderabad, Telangana 500081",
        "category": "Service Providers",
        "contact_person": "Amit Patel",
        "designation": "Director - Cloud Solutions",
        "alternate_phone": "9334500890",
        "gst_number": "36AADCC9012M1Z3",
        "pan_number": "AADCC9012M",
        "company_registration_number": "U72900TG2019PTC131204",
        "address_line_1": "Level 6, Cyber Towers, HITEC City",
        "address_line_2": "Madhapur",
        "city": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "pincode": "500081",
        "website": "https://www.cloudinfra.io",
        "description": (
            "AWS and Azure Advanced Consulting Partner delivering cloud migration, FinOps and "
            "24x7 managed operations. Maintains ISO 27001 certified security practices."
        ),
        "bank_account_number": "10023456789012",
        "ifsc_code": "AXIS0000789",
        "payment_terms": "Net 30",
        "delivery_score": 94.0,
        "quality_score": 92.0,
        "communication_score": 96.0,
        "service_score": 90.0,
        "reliability_score": 93.0,
        "status": "Active",
        "approval_status": "Approved",
        "approved_by": "Admin User",
    },
    {
        "vendor_name": "Suresh Reddy",
        "company_name": "BuildRight Materials",
        "email": "suresh@buildright.in",
        "phone": "9445678901",
        "address": "Road No 36, Jubilee Hills, Hyderabad, Telangana 500033",
        "category": "Raw Material Suppliers",
        "contact_person": "Suresh Reddy",
        "designation": "Proprietor",
        "alternate_phone": "9445600901",
        "gst_number": "36AAFCB3456N1Z7",
        "pan_number": "AAFCB3456N",
        "company_registration_number": "U26940TG2012PTC081337",
        "address_line_1": "Plot 219, Road No 36",
        "address_line_2": "Jubilee Hills",
        "city": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "pincode": "500033",
        "website": "https://www.buildrightmaterials.in",
        "description": (
            "Bulk supplier of TMT steel, cement and aggregates for infrastructure projects across "
            "Telangana and Andhra Pradesh. Operates its own fleet for site delivery."
        ),
        "bank_account_number": "678901234567",
        "ifsc_code": "KKBK0005678",
        "payment_terms": "Net 60",
        "delivery_score": 70.0,
        "quality_score": 76.0,
        "communication_score": 64.0,
        "service_score": 72.0,
        "reliability_score": 70.4,
        "status": "Active",
        "approval_status": "Approved",
        "approved_by": "Admin User",
    },
    {
        "vendor_name": "Kavitha Nair",
        "company_name": "GreenPack Logistics",
        "email": "kavitha@greenpack.in",
        "phone": "9556789012",
        "address": "Willingdon Island, Kochi, Kerala 682003",
        "category": "Logistics Partners",
        "contact_person": "Kavitha Nair",
        "designation": "Founder & CEO",
        "alternate_phone": "9556700012",
        "gst_number": "32AAGCG7890P1Z1",
        "pan_number": "AAGCG7890P",
        "company_registration_number": "U63030KL2023PTC079005",
        "address_line_1": "Warehouse 12, Willingdon Island",
        "address_line_2": "Port Trust Road",
        "city": "Kochi",
        "state": "Kerala",
        "country": "India",
        "pincode": "682003",
        "website": "https://www.greenpacklogistics.in",
        "description": (
            "Sustainable packaging and last-mile logistics start-up using recycled materials. "
            "Newly registered on the platform and awaiting compliance verification."
        ),
        "bank_account_number": "789012345678",
        "ifsc_code": "FDRL0001234",
        "payment_terms": "Net 30",
        "delivery_score": 0.0,
        "quality_score": 0.0,
        "communication_score": 0.0,
        "service_score": 0.0,
        "reliability_score": 0.0,
        "status": "Pending",
        "approval_status": "Pending",
        "approved_by": None,
    },
]


def _pending_seed_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_seed_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_seed_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_seed_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_seed_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_seed_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_seed_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_seed_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_seed_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_seed_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
