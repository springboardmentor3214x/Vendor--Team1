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

PROCUREMENT_PLAN = [
    ("IT Laptop Fleet Refresh", "IT Department", "Rajesh Kumar", "Dell Laptops (Latitude 5540)",
     "IT Equipment", "TechSupply India Pvt Ltd", 25, 72000.0, "High", "Completed", "Approved", 380, 355, -2),
    ("Ergonomic Workstation Setup", "Operations", "Priya Sharma", "Office Chairs (Ergonomic)",
     "Furniture", "OfficeMart Solutions", 50, 8500.0, "Medium", "Completed", "Approved", 340, 315, 3),
    ("AWS Cloud Hosting Subscription", "IT Department", "Amit Patel", "AWS Cloud Credits (Annual)",
     "Cloud Services", "CloudInfra Services", 1, 500000.0, "Critical", "Completed", "Approved", 300, 285, 0),
    ("Construction Material Supply - Phase 1", "Logistics", "Suresh Reddy", "Steel Rods (TMT 500D)",
     "Raw Materials", "BuildRight Materials", 200, 4500.0, "High", "Completed", "Approved", 270, 245, 4),
    ("Core Network Infrastructure Update", "IT Department", "Rajesh Kumar", "Networking Switches (Cisco)",
     "IT Equipment", "TechSupply India Pvt Ltd", 10, 35000.0, "High", "Delivered", "Approved", 230, 205, 0),
    ("Office Stationery Restock Q3", "Administration", "Anita Desai", "Printer Paper (A4, 5000 sheets)",
     "Office Supplies", "OfficeMart Solutions", 100, 350.0, "Low", "Completed", "Approved", 200, 180, 0),
    ("Azure DevOps Licensing", "IT Department", "Amit Patel", "Azure DevOps Licenses",
     "Software Licenses", "CloudInfra Services", 30, 12000.0, "Medium", "Delivered", "Approved", 175, 155, -1),
    ("Reception & Meeting Room Furniture", "Administration", "Anita Desai", "Office Furniture (Modular)",
     "Furniture", "OfficeMart Solutions", 20, 24000.0, "Medium", "Delivered", "Approved", 150, 128, -1),
    ("Perimeter Security Upgrade", "Operations", "Mohan Iyer", "Security Cameras (IP, 4K)",
     "IT Equipment", "TechSupply India Pvt Ltd", 40, 15500.0, "High", "Completed", "Approved", 130, 108, 1),
    ("Data Centre Server Expansion", "IT Department", "Rajesh Kumar", "Server Hardware (Rack Mount)",
     "IT Equipment", "TechSupply India Pvt Ltd", 6, 285000.0, "Critical", "Delivered", "Approved", 105, 82, 0),
    ("Civil Foundation Materials", "Logistics", "Suresh Reddy", "Cement Bags (OPC 53 Grade)",
     "Raw Materials", "BuildRight Materials", 500, 380.0, "Medium", "Delivered", "Approved", 85, 62, 6),
    ("Warehouse Packaging Materials", "Logistics", "Mohan Iyer", "Packaging Materials (Recycled)",
     "Packaging", "OfficeMart Solutions", 300, 220.0, "Low", "Completed", "Approved", 70, 50, 2),
    ("Enterprise Endpoint Security Rollout", "IT Department", "Vikram Shah", "Endpoint Security Licenses",
     "Software Licenses", "Global Vendor Solutions", 250, 3200.0, "High", "Completed", "Approved", 320, 300, -1),
    ("Managed Print Services Hardware", "Administration", "Anita Desai", "Multifunction Printers",
     "IT Equipment", "Global Vendor Solutions", 18, 62000.0, "Medium", "Completed", "Approved", 240, 218, 0),
    ("Conference Room AV Upgrade", "Operations", "Mohan Iyer", "Video Conferencing Systems",
     "IT Equipment", "Global Vendor Solutions", 12, 145000.0, "Medium", "Delivered", "Approved", 115, 95, 0),
    ("Site Safety Equipment", "Operations", "Mohan Iyer", "Safety Equipment (Helmets & Vests)",
     "Safety", "BuildRight Materials", 120, 950.0, "High", "Ordered", "Approved", 32, 8, None),
    ("Facility Cleaning Supplies", "Administration", "Anita Desai", "Cleaning Supplies (Industrial)",
     "Consumables", "OfficeMart Solutions", 150, 480.0, "Low", "Ordered", "Approved", 45, 12, None),
    ("Annual Conference Merchandise", "Marketing", "Neha Kapoor", "Branded Merchandise Kits",
     "Marketing", "OfficeMart Solutions", 500, 640.0, "Medium", "Ordered", "Approved", 25, 15, None),
    ("Finance Team Workstation Upgrade", "Finance", "Vikram Shah", "Dell Laptops (Latitude 5540)",
     "IT Equipment", "TechSupply India Pvt Ltd", 12, 72000.0, "Medium", "Approved", "Approved", 18, 30, None),
    ("HR Onboarding Kits", "Human Resources", "Neha Kapoor", "Office Furniture (Modular)",
     "Furniture", "OfficeMart Solutions", 15, 24000.0, "Medium", "Pending", "Pending", 9, 45, None),
    ("Cloud Backup & DR Subscription", "IT Department", "Amit Patel", "AWS Cloud Credits (Annual)",
     "Cloud Services", "CloudInfra Services", 1, 320000.0, "High", "Pending", "Pending", 4, 60, None),
]

EXTRA_PROCUREMENTS = [
    ("Bulk Aggregate Purchase", "Logistics", "Suresh Reddy", "Construction Aggregates",
     "Raw Materials", "BuildRight Materials", 800, 290.0, "Low", "Cancelled", "Rejected", 60, 30),
    ("Marketing Collateral Redesign", "Marketing", "Neha Kapoor", "Printed Brochures",
     "Marketing", "OfficeMart Solutions", 2000, 45.0, "Low", "Modification Required", "Modification Required", 11, 40),
]

VENDOR_PROFILE = {
    "CloudInfra Services": {
        "quality": (5, 5, 5, 5), "defects": 0, "rating": 5.0, "response_hours": 1.5,
        "service": (5, 5, 5, 4, 5, 5), "service_rating": 4.8,
        "quality_note": "Flawless provisioning; all entitlements activated ahead of schedule.",
        "service_note": "Outstanding partner — proactive updates and rapid escalation handling.",
    },
    "Global Vendor Solutions": {
        "quality": (5, 4, 5, 5), "defects": 0, "rating": 4.6, "response_hours": 2.5,
        "service": (5, 4, 5, 4, 4, 5), "service_rating": 4.5,
        "quality_note": "Complete consignment received in specification with sealed packaging.",
        "service_note": "Dependable delivery partner with clear documentation.",
    },
    "TechSupply India Pvt Ltd": {
        "quality": (5, 4, 5, 4), "defects": 1, "rating": 4.4, "response_hours": 3.0,
        "service": (4, 4, 5, 4, 4, 4), "service_rating": 4.2,
        "quality_note": "All units functional; one carton showed minor transit scuffing.",
        "service_note": "Reliable IT hardware vendor with competitive pricing and good paperwork.",
    },
    "OfficeMart Solutions": {
        "quality": (4, 3, 5, 4), "defects": 2, "rating": 3.8, "response_hours": 6.0,
        "service": (4, 3, 4, 4, 3, 4), "service_rating": 3.7,
        "quality_note": "Acceptable quality; two items required on-site adjustment after delivery.",
        "service_note": "Decent service overall — response times could be faster during peak periods.",
    },
    "BuildRight Materials": {
        "quality": (4, 3, 4, 3), "defects": 3, "rating": 3.2, "response_hours": 18.0,
        "service": (3, 3, 3, 3, 2, 3), "service_rating": 2.9,
        "quality_note": "Material grade verified, but consignment arrived short and required a top-up load.",
        "service_note": "Frequent schedule slippage and slow responses to written queries.",
    },
}


def _pending_seed_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "reference", "")),
            "state": getattr(item, "status", "New"),
        })
    return rows


def _pending_seed_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    totals["ratio"] = round(
        totals["active"] / totals["count"], 2) if totals["count"] else 0.0
    return totals


def _pending_seed_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "reference", "")),
            "state": getattr(item, "status", "New"),
        })
    return rows


def _pending_seed_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    totals["ratio"] = round(
        totals["active"] / totals["count"], 2) if totals["count"] else 0.0
    return totals


def _pending_seed_rows_3(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "reference", "")),
            "state": getattr(item, "status", "New"),
        })
    return rows


def _pending_seed_totals_3(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    totals["ratio"] = round(
        totals["active"] / totals["count"], 2) if totals["count"] else 0.0
    return totals


def _pending_seed_rows_4(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "reference", "")),
            "state": getattr(item, "status", "New"),
        })
    return rows


def _pending_seed_totals_4(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    totals["ratio"] = round(
        totals["active"] / totals["count"], 2) if totals["count"] else 0.0
    return totals


def _pending_seed_rows_5(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "reference", "")),
            "state": getattr(item, "status", "New"),
        })
    return rows


def _pending_seed_totals_5(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    totals["ratio"] = round(
        totals["active"] / totals["count"], 2) if totals["count"] else 0.0
    return totals
