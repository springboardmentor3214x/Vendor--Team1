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


def seed_database(reset: bool = False):
    if reset:
        from sqlalchemy import text
        with engine.connect() as conn:
            try:
                conn.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();"))
                conn.commit()
            except Exception:
                pass
            try:
                conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
                conn.commit()
            except Exception as e:
                print(f"Schema drop warning: {e}")
                Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    now = datetime.utcnow()
    today = date.today()

    try:
        print("Seeding users...")
        user_ids = {}
        for u in DEFAULT_USERS:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if existing:
                user_ids[u["email"]] = existing.id
                continue
            db_user = User(
                name=u["name"],
                email=u["email"],
                mobile_number=u["mobile_number"],
                password=hash_password(u["password"]),
                role=u["role"],
                account_status="Active",
            )
            db.add(db_user)
            db.flush()
            user_ids[u["email"]] = db_user.id

        print("Seeding vendors...")
        vendor_ids = {}
        vendors_by_name = {}
        for v in DEFAULT_VENDORS:
            existing_v = db.query(Vendor).filter(Vendor.company_name == v["company_name"]).first()
            if existing_v:
                vendor_ids[v["company_name"]] = existing_v.id
                vendors_by_name[v["company_name"]] = existing_v
                continue

            approved = v["approval_status"] == "Approved"
            vendor = Vendor(
                **v,
                created_by="Admin User",
                created_at=now - timedelta(days=400),
                updated_by="Admin User",
                updated_at=now - timedelta(days=30),
                approved_at=(now - timedelta(days=395)) if approved else None,
            )
            db.add(vendor)
            db.flush()
            vendor_ids[v["company_name"]] = vendor.id
            vendors_by_name[v["company_name"]] = vendor

        if db.query(Procurement).count() > 0:
            print("Transactional data already present — skipping procurement/PO/invoice seed.")
            db.commit()
            return

        print("Seeding procurements...")
        procurements = []
        fulfilment_plan = []

        seq = 0
        for (title, dept, requester, item, category, vendor_company, qty, unit_price,
             priority, status, approval_status, days_ago, days_to_expected, offset) in PROCUREMENT_PLAN:
            seq += 1
            created = now - timedelta(days=days_ago)
            expected = now - timedelta(days=days_to_expected)
            actual = None
            if offset is not None and status in ("Delivered", "Completed"):
                actual = expected + timedelta(days=offset)

            proc = Procurement(
                request_number=f"PR-2026-{seq:04d}",
                request_title=title,
                department=dept,
                requested_by=requester,
                item_name=item,
                category=category,
                vendor_id=vendor_ids[vendor_company],
                quantity=qty,
                unit_of_measurement="Units",
                unit_price=unit_price,
                total_price=qty * unit_price,
                priority=priority,
                business_justification=f"Required to support planned {dept} operations for the current financial year.",
                remarks="Approved within standard procurement policy limits." if approval_status == "Approved" else None,
                status=status,
                approval_status=approval_status,
                approved_by="Procurement Manager" if approval_status == "Approved" else None,
                expected_delivery_date=expected,
                actual_delivery_date=actual,
                created_at=created,
            )
            procurements.append(proc)
            fulfilment_plan.append((proc, vendor_company, status, offset, expected, created))

        for (title, dept, requester, item, category, vendor_company, qty, unit_price,
             priority, status, approval_status, days_ago, days_to_expected) in EXTRA_PROCUREMENTS:
            seq += 1
            proc = Procurement(
                request_number=f"PR-2026-{seq:04d}",
                request_title=title,
                department=dept,
                requested_by=requester,
                item_name=item,
                category=category,
                vendor_id=vendor_ids[vendor_company],
                quantity=qty,
                unit_of_measurement="Units",
                unit_price=unit_price,
                total_price=qty * unit_price,
                priority=priority,
                business_justification=f"Requested by {dept} to cover planned activity.",
                remarks=("Rejected — budget reallocated to higher-priority projects."
                         if approval_status == "Rejected"
                         else "Sent back: attach three comparative quotations before resubmitting."),
                status=status,
                approval_status=approval_status,
                approved_by="Admin User" if approval_status == "Rejected" else None,
                expected_delivery_date=now + timedelta(days=days_to_expected),
                created_at=now - timedelta(days=days_ago),
            )
            procurements.append(proc)

        db.add_all(procurements)
        db.flush()

        history_rows = []
        for proc in procurements:
            history_rows.append(ProcurementStatusHistory(
                procurement_id=proc.id, status="Pending", updated_by=proc.requested_by,
                remarks="Procurement Request Created", created_at=proc.created_at
            ))
            if proc.approval_status == "Approved":
                history_rows.append(ProcurementStatusHistory(
                    procurement_id=proc.id, status="Approved", updated_by="Procurement Manager",
                    remarks="Approved within budget", created_at=proc.created_at + timedelta(days=1)
                ))
            if proc.status in ("Ordered", "Delivered", "Completed"):
                history_rows.append(ProcurementStatusHistory(
                    procurement_id=proc.id, status="Ordered", updated_by="Procurement Manager",
                    remarks="Purchase Order issued", created_at=proc.created_at + timedelta(days=3)
                ))
            if proc.status in ("Delivered", "Completed") and proc.actual_delivery_date:
                history_rows.append(ProcurementStatusHistory(
                    procurement_id=proc.id, status="Delivered", updated_by="Supply Chain Manager",
                    remarks="Goods received at warehouse", created_at=proc.actual_delivery_date
                ))
            if proc.status == "Completed" and proc.actual_delivery_date:
                history_rows.append(ProcurementStatusHistory(
                    procurement_id=proc.id, status="Completed", updated_by="Finance Manager",
                    remarks="Invoice verified and payment released",
                    created_at=proc.actual_delivery_date + timedelta(days=5)
                ))
        db.add_all(history_rows)

        print("Seeding purchase orders, tracking and invoices...")
        purchase_orders = []
        tracking_rows = []
        invoices = []
        payment_cycle = ["Paid", "Paid", "Approved", "Paid", "Approved", "Verified",
                         "Approved", "Verified", "Pending", "Pending"]

        po_seq = 0
        inv_seq = 0
        for proc, vendor_company, status, offset, expected, created in fulfilment_plan:
            if status not in ("Ordered", "Delivered", "Completed"):
                continue

            vendor = vendors_by_name[vendor_company]
            po_seq += 1
            po_date = created + timedelta(days=2)
            base_cost = proc.total_price
            tax_amount = round(base_cost * GST_RATE, 2)

            po_status = {
                "Ordered": "In Transit",
                "Delivered": "Delivered",
                "Completed": "Completed",
            }[status]

            po = PurchaseOrder(
                po_number=f"PO-2026-{po_seq:04d}",
                procurement_id=proc.id,
                vendor_id=vendor.id,
                vendor_name=vendor.company_name,
                vendor_address=vendor.address_line_1,
                contact_person=vendor.contact_person,
                item_name=proc.item_name,
                quantity=proc.quantity,
                unit_price=proc.unit_price,
                total_cost=base_cost,
                tax_amount=tax_amount,
                shipping_address=SHIPPING_ADDRESS,
                expected_delivery_date=expected,
                payment_terms=vendor.payment_terms or "Net 30",
                status=po_status,
                approved_by="Procurement Manager",
                po_date=po_date,
            )
            purchase_orders.append(po)
            db.add(po)
            db.flush()

            dispatch_date = po_date + timedelta(days=4)
            actual_delivery = proc.actual_delivery_date

            if status == "Ordered":
                delivery_status = "In Transit"
                delay_status = "Delayed" if expected < now else "On Time"
                delay_days = max((now - expected).days, 0) if expected < now else 0
                delay_hours = delay_days * 24
            else:
                _, delay_hours, delay_days = delivery_status_from_times(expected, actual_delivery)
                delivery_status = "Completed" if status == "Completed" else "Delivered"
                delay_status = "Delayed" if delay_hours > 0 else "On Time"

            tracking_rows.append(OrderTracking(
                po_id=po.id,
                procurement_id=proc.id,
                vendor_id=vendor.id,
                dispatch_date=dispatch_date,
                expected_delivery_date=expected,
                actual_delivery_date=actual_delivery,
                delivery_status=delivery_status,
                delay_status=delay_status,
                delay_hours=int(delay_hours),
                delay_days=int(delay_days),
                updated_at=actual_delivery or now,
            ))

            if status in ("Delivered", "Completed") and actual_delivery:
                inv_seq += 1
                invoice_date = actual_delivery + timedelta(days=2)
                payment_status = "Paid" if status == "Completed" else payment_cycle[inv_seq % len(payment_cycle)]
                invoices.append(Invoice(
                    invoice_number=f"INV-2026-{inv_seq:04d}",
                    po_id=po.id,
                    procurement_id=proc.id,
                    vendor_id=vendor.id,
                    vendor_name=vendor.company_name,
                    invoice_date=invoice_date,
                    due_date=invoice_date + timedelta(days=30),
                    invoice_amount=base_cost,
                    tax_amount=tax_amount,
                    total_amount=base_cost + tax_amount,
                    payment_status=payment_status,
                    verified_by="Finance Manager" if payment_status != "Pending" else None,
                    approved_by="Finance Manager" if payment_status in ("Approved", "Paid") else None,
                    remarks=f"Invoice for {proc.item_name} against {po.po_number}",
                ))

        db.add_all(tracking_rows)
        db.add_all(invoices)

        print("Seeding performance records...")
        delivery_records = []
        quality_records = []
        comm_logs = []
        service_records = []

        for proc, vendor_company, status, offset, expected, created in fulfilment_plan:
            vendor = vendors_by_name[vendor_company]
            profile = VENDOR_PROFILE[vendor_company]

            sent_time = created + timedelta(days=1)
            responded = status != "Ordered" or vendor_company != "BuildRight Materials"
            comm_logs.append(CommunicationLog(
                vendor_id=vendor.id,
                procurement_id=proc.id,
                message_sent_time=sent_time,
                vendor_response_time=(sent_time + timedelta(hours=profile["response_hours"])) if responded else None,
                response_duration_hours=profile["response_hours"] if responded else None,
                communication_status="Responded" if responded else "Pending",
                remarks=(f"Schedule confirmation for {proc.item_name}" if responded
                         else "Awaiting vendor confirmation on revised schedule"),
            ))

            if status not in ("Delivered", "Completed") or not proc.actual_delivery_date:
                continue

            actual = proc.actual_delivery_date
            delivery_records.append(_delivery_row(
                vendor.id, proc.id, expected, actual,
                ("Delivered ahead of schedule" if offset < 0 else
                 "Delivered on the agreed date" if offset == 0 else
                 f"Delivered {offset} day(s) behind schedule"),
            ))

            mq, pq, qa, sc = profile["quality"]
            quality_records.append(QualityEvaluation(
                vendor_id=vendor.id,
                procurement_id=proc.id,
                inspection_date=actual + timedelta(days=1),
                material_quality=mq,
                packaging_quality=pq,
                quantity_accuracy=qa,
                specification_compliance=sc,
                defect_count=profile["defects"],
                overall_rating=profile["rating"],
                remarks=f"{proc.item_name}: {profile['quality_note']}",
            ))

            if status == "Completed":
                prof, support, docs, flex, comm_eff, issue = profile["service"]
                service_records.append(ServiceRating(
                    vendor_id=vendor.id,
                    procurement_id=proc.id,
                    professionalism=prof,
                    customer_support=support,
                    documentation_quality=docs,
                    flexibility=flex,
                    communication_effectiveness=comm_eff,
                    issue_resolution=issue,
                    overall_rating=profile["service_rating"],
                    comments=profile["service_note"],
                    rated_at=actual + timedelta(days=6),
                ))

        db.add_all(delivery_records)
        db.add_all(quality_records)
        db.add_all(comm_logs)
        db.add_all(service_records)

        print("Seeding contracts...")
        contracts = [
            Contract(
                contract_number="CTR-2026-0001",
                contract_title="Annual IT Hardware Maintenance & Licensing Agreement",
                vendor_id=vendor_ids["TechSupply India Pvt Ltd"],
                vendor_name="TechSupply India Pvt Ltd",
                contract_type="Master Agreement",
                procurement_category="IT Equipment",
                start_date=today - timedelta(days=120),
                end_date=today + timedelta(days=245),
                contract_value=1200000.0,
                payment_terms="Net 45",
                sla_details="Next-business-day on-site replacement; 99.5% hardware availability; monthly service review.",
                warranty_details="36 months comprehensive warranty on all supplied hardware including parts and labour.",
                responsible_manager="Procurement Manager",
                status="Active",
                created_at=now - timedelta(days=120),
            ),
            Contract(
                contract_number="CTR-2026-0002",
                contract_title="Office Supplies Master Agreement - v2",
                vendor_id=vendor_ids["OfficeMart Solutions"],
                vendor_name="OfficeMart Solutions",
                contract_type="Rate Contract",
                procurement_category="Office Supplies",
                start_date=today - timedelta(days=340),
                end_date=today + timedelta(days=22),
                contract_value=450000.0,
                payment_terms="Net 30",
                sla_details="Delivery within 5 working days of purchase order; replacement of damaged goods within 48 hours.",
                warranty_details="12 months warranty on furniture; consumables covered by manufacturer warranty.",
                responsible_manager="Procurement Manager",
                status="Expiring Soon",
                created_at=now - timedelta(days=340),
            ),
            Contract(
                contract_number="CTR-2026-0003",
                contract_title="AWS Multi-Account Support & Optimisation SLA",
                vendor_id=vendor_ids["CloudInfra Services"],
                vendor_name="CloudInfra Services",
                contract_type="Service Level Agreement",
                procurement_category="Cloud Services",
                start_date=today - timedelta(days=90),
                end_date=today + timedelta(days=275),
                contract_value=2400000.0,
                payment_terms="Net 30",
                sla_details="24x7 support, 15-minute response for Severity-1 incidents, 99.95% uptime commitment.",
                warranty_details="Service credits payable for any month falling below the committed uptime.",
                responsible_manager="Supply Chain Manager",
                status="Active",
                created_at=now - timedelta(days=90),
            ),
            Contract(
                contract_number="CTR-2026-0004",
                contract_title="Bulk Steel & Cement Supply Agreement",
                vendor_id=vendor_ids["BuildRight Materials"],
                vendor_name="BuildRight Materials",
                contract_type="Supply Agreement",
                procurement_category="Raw Materials",
                start_date=today - timedelta(days=430),
                end_date=today - timedelta(days=65),
                contract_value=1850000.0,
                payment_terms="Net 60",
                sla_details="Site delivery within 7 days of release order; mill test certificates with every consignment.",
                warranty_details="Material conformance to IS 1786 guaranteed; rejected lots replaced at vendor cost.",
                responsible_manager="Procurement Manager",
                status="Expired",
                created_at=now - timedelta(days=430),
            ),
            Contract(
                contract_number="CTR-2026-0005",
                contract_title="Enterprise IT Managed Services Agreement",
                vendor_id=vendor_ids["Global Vendor Solutions"],
                vendor_name="Global Vendor Solutions",
                contract_type="Master Agreement",
                procurement_category="IT Equipment",
                start_date=today - timedelta(days=200),
                end_date=today + timedelta(days=530),
                contract_value=980000.0,
                payment_terms="Net 30",
                sla_details="Quarterly asset audit, 4-hour remote response, dedicated account manager.",
                warranty_details="24 months warranty on all supplied equipment.",
                responsible_manager="Procurement Manager",
                status="Active",
                created_at=now - timedelta(days=200),
            ),
            Contract(
                contract_number="CTR-2026-0006",
                contract_title="Sustainable Packaging & Last-Mile Logistics (Draft)",
                vendor_id=vendor_ids["GreenPack Logistics"],
                vendor_name="GreenPack Logistics",
                contract_type="Service Agreement",
                procurement_category="Packaging",
                start_date=today + timedelta(days=15),
                end_date=today + timedelta(days=380),
                contract_value=620000.0,
                payment_terms="Net 30",
                sla_details="Pending finalisation — proposed 48-hour dispatch commitment for all metro destinations.",
                warranty_details="To be agreed during contract negotiation.",
                responsible_manager="Supply Chain Manager",
                status="Draft",
                created_at=now - timedelta(days=10),
            ),
        ]
        db.add_all(contracts)
        db.flush()

        print("Seeding certifications...")
        certifications = [
            ("TechSupply India Pvt Ltd", "ISO 9001:2015", "ISO-9001-TSI-4471", "Bureau Veritas India", 700, 400, "Active"),
            ("TechSupply India Pvt Ltd", "GST Registration", "09AABCT1234F1Z5", "GST Council of India", 900, 1200, "Active"),
            ("OfficeMart Solutions", "ISO 9001:2015", "ISO-9001-OMS-2210", "TUV SUD South Asia", 720, 18, "Expiring Soon"),
            ("OfficeMart Solutions", "Business License", "BL-KA-2019-88213", "BBMP Bangalore", 600, 300, "Active"),
            ("CloudInfra Services", "ISO 27001:2022", "ISO-27001-CIS-9087", "BSI Group India", 400, 720, "Active"),
            ("CloudInfra Services", "GST Registration", "36AADCC9012M1Z3", "GST Council of India", 850, 1100, "Active"),
            ("CloudInfra Services", "Cyber Security Audit Clearance", "CERT-IN-2025-4409", "CERT-In Empanelled Auditor", 300, 430, "Active"),
            ("BuildRight Materials", "Manufacturing License", "ML-TG-2018-33119", "Telangana Industries Dept", 1100, -45, "Expired"),
            ("BuildRight Materials", "Environmental Clearance", "EC-TG-2021-7742", "Telangana Pollution Control Board", 800, 260, "Active"),
            ("Global Vendor Solutions", "ISO 9001:2015", "ISO-9001-GVS-1180", "Bureau Veritas India", 640, 500, "Active"),
            ("Global Vendor Solutions", "GST Registration", "06AABCG1234H1Z2", "GST Council of India", 940, 1300, "Active"),
        ]
        db.add_all([
            Certification(
                vendor_id=vendor_ids[company],
                certification_name=name,
                certificate_number=number,
                issuing_authority=authority,
                issue_date=today - timedelta(days=issued_days_ago),
                expiry_date=today + timedelta(days=expires_in_days),
                status=status,
                created_at=now - timedelta(days=issued_days_ago),
            )
            for company, name, number, authority, issued_days_ago, expires_in_days, status in certifications
        ])

        print("Seeding compliance records...")
        compliance_rows = [
            ("TechSupply India Pvt Ltd", "GST Compliance", "Compliant", "Auditor User", 40, 320,
             "GSTR filings current through the last quarter."),
            ("TechSupply India Pvt Ltd", "ISO Compliance", "Compliant", "Auditor User", 60, 400,
             "Surveillance audit passed with no major non-conformities."),
            ("OfficeMart Solutions", "Tax Compliance", "Compliant", "Auditor User", 55, 300,
             "TDS and advance tax obligations verified."),
            ("OfficeMart Solutions", "ISO Compliance", "Pending Verification", None, None, 18,
             "Renewed ISO certificate requested from vendor; awaiting upload."),
            ("CloudInfra Services", "Cybersecurity Standards", "Compliant", "Auditor User", 30, 430,
             "CERT-In audit report reviewed and accepted."),
            ("CloudInfra Services", "GST Compliance", "Compliant", "Auditor User", 45, 350,
             "All returns filed on time."),
            ("BuildRight Materials", "Environmental Compliance", "Non-Compliant", "Auditor User", 25, -45,
             "Manufacturing licence lapsed; consent-to-operate renewal not submitted."),
            ("BuildRight Materials", "Labor Law Compliance", "Pending Verification", None, None, 90,
             "Contract labour register pending inspection."),
            ("Global Vendor Solutions", "GST Compliance", "Compliant", "Auditor User", 35, 380,
             "No outstanding demands or notices."),
        ]
        db.add_all([
            ComplianceRecord(
                vendor_id=vendor_ids[company],
                compliance_type=ctype,
                status=status,
                verified_by=verified_by,
                verification_date=(today - timedelta(days=verified_days_ago)) if verified_days_ago else None,
                expiry_date=today + timedelta(days=expires_in_days),
                remarks=remarks,
                created_at=now - timedelta(days=verified_days_ago or 20),
            )
            for company, ctype, status, verified_by, verified_days_ago, expires_in_days, remarks in compliance_rows
        ])

        print("Seeding vendor documents...")
        document_types = ["GST Certificate", "PAN Card", "Company Registration Certificate"]
        db.add_all([
            VendorDocument(
                vendor_id=vendor_ids[company],
                document_type=doc_type,
                file_name=f"{company.split()[0].lower()}_{doc_type.split()[0].lower()}.pdf",
                file_path=f"static/vendor_documents/{vendor_ids[company]}/{company.split()[0].lower()}_{doc_type.split()[0].lower()}.pdf",
                uploaded_at=now - timedelta(days=390),
            )
            for company in vendor_ids
            for doc_type in document_types
        ])

        print("Seeding discussions and communications...")
        discussions = [
            Discussion(
                topic="Delivery Schedule Change - PO-2026-0011",
                vendor_id=vendor_ids["BuildRight Materials"],
                procurement_id=procurements[10].id,
                po_id=purchase_orders[10].id if len(purchase_orders) > 10 else None,
                created_by="Procurement Manager",
                status="Resolved",
                created_at=now - timedelta(days=64),
            ),
            Discussion(
                topic="Invoice Discrepancy - INV-2026-0002",
                vendor_id=vendor_ids["OfficeMart Solutions"],
                procurement_id=procurements[1].id,
                created_by="Finance Manager",
                status="Resolved",
                created_at=now - timedelta(days=305),
            ),
            Discussion(
                topic="Contract Renewal Terms Discussion - CTR-2026-0002",
                vendor_id=vendor_ids["OfficeMart Solutions"],
                contract_id=contracts[1].id,
                created_by="Procurement Manager",
                status="Active",
                created_at=now - timedelta(days=12),
            ),
            Discussion(
                topic="Quality Escalation - Steel Consignment Shortfall",
                vendor_id=vendor_ids["BuildRight Materials"],
                procurement_id=procurements[3].id,
                created_by="Supply Chain Manager",
                status="Active",
                created_at=now - timedelta(days=240),
            ),
        ]
        db.add_all(discussions)
        db.flush()

        comms = [
            Communication(
                procurement_id=procurements[0].id,
                vendor_id=vendor_ids["TechSupply India Pvt Ltd"],
                sender_name="Procurement Manager",
                message="Hi Rajesh, could you share a tracking update for the Dell Latitude consignment?",
                is_read=True,
                sent_at=now - timedelta(days=360),
            ),
            Communication(
                procurement_id=procurements[0].id,
                vendor_id=vendor_ids["TechSupply India Pvt Ltd"],
                sender_name="Rajesh Kumar",
                message="Dispatched this morning via Blue Dart. Expected at your Gurgaon dock in 48 hours.",
                is_read=True,
                sent_at=now - timedelta(days=359),
            ),
            Communication(
                procurement_id=procurements[1].id,
                vendor_id=vendor_ids["OfficeMart Solutions"],
                sender_name="Procurement Manager",
                message="Priya, we received the chairs but two units have unstable armrests.",
                is_read=True,
                sent_at=now - timedelta(days=310),
            ),
            Communication(
                procurement_id=procurements[1].id,
                vendor_id=vendor_ids["OfficeMart Solutions"],
                sender_name="Priya Sharma",
                message="Apologies for that. A service technician will visit tomorrow to replace both units.",
                is_read=True,
                sent_at=now - timedelta(days=309),
            ),
            Communication(
                procurement_id=procurements[3].id,
                vendor_id=vendor_ids["BuildRight Materials"],
                discussion_id=discussions[3].id,
                sender_name="Supply Chain Manager",
                message="Suresh, the TMT consignment is 12 tonnes short against the release order. Please confirm the top-up schedule.",
                is_read=True,
                sent_at=now - timedelta(days=240),
            ),
            Communication(
                procurement_id=procurements[3].id,
                vendor_id=vendor_ids["BuildRight Materials"],
                discussion_id=discussions[3].id,
                sender_name="Suresh Reddy",
                message="Acknowledged. The balance quantity will be dispatched from our Medak yard within four days.",
                is_read=True,
                sent_at=now - timedelta(days=238),
            ),
            Communication(
                procurement_id=procurements[2].id,
                vendor_id=vendor_ids["CloudInfra Services"],
                sender_name="Amit Patel",
                message="All AWS credits have been applied to your linked accounts. Billing console reflects the update.",
                is_read=True,
                sent_at=now - timedelta(days=284),
            ),
            Communication(
                contract_id=contracts[1].id,
                vendor_id=vendor_ids["OfficeMart Solutions"],
                discussion_id=discussions[2].id,
                sender_name="Procurement Manager",
                message="Priya, CTR-2026-0002 expires in three weeks. Please share revised rate cards for renewal.",
                is_read=False,
                sent_at=now - timedelta(days=12),
            ),
            Communication(
                contract_id=contracts[1].id,
                vendor_id=vendor_ids["OfficeMart Solutions"],
                discussion_id=discussions[2].id,
                sender_name="Priya Sharma",
                message="Revised rate card is being finalised and will be uploaded by the end of this week.",
                is_read=False,
                sent_at=now - timedelta(days=10),
            ),
            Communication(
                procurement_id=procurements[15].id,
                vendor_id=vendor_ids["BuildRight Materials"],
                sender_name="Procurement Manager",
                message="Suresh, the safety equipment order is approaching its delivery date. Please confirm dispatch.",
                is_read=False,
                sent_at=now - timedelta(days=3),
            ),
        ]
        db.add_all(comms)

        db.add_all([
            SharedFile(
                file_name="techsupply_delivery_challan.pdf",
                file_path=f"static/shared_files/{vendor_ids['TechSupply India Pvt Ltd']}/techsupply_delivery_challan.pdf",
                file_type="application/pdf",
                file_size=248_320,
                uploaded_by="Rajesh Kumar",
                vendor_id=vendor_ids["TechSupply India Pvt Ltd"],
                procurement_id=procurements[0].id,
                created_at=now - timedelta(days=358),
            ),
            SharedFile(
                file_name="officemart_revised_rate_card.xlsx",
                file_path=f"static/shared_files/{vendor_ids['OfficeMart Solutions']}/officemart_revised_rate_card.xlsx",
                file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                file_size=61_440,
                uploaded_by="Priya Sharma",
                vendor_id=vendor_ids["OfficeMart Solutions"],
                contract_id=contracts[1].id,
                discussion_id=discussions[2].id,
                created_at=now - timedelta(days=10),
            ),
            SharedFile(
                file_name="buildright_mill_test_certificate.pdf",
                file_path=f"static/shared_files/{vendor_ids['BuildRight Materials']}/buildright_mill_test_certificate.pdf",
                file_type="application/pdf",
                file_size=512_000,
                uploaded_by="Suresh Reddy",
                vendor_id=vendor_ids["BuildRight Materials"],
                procurement_id=procurements[3].id,
                discussion_id=discussions[3].id,
                created_at=now - timedelta(days=239),
            ),
        ])

        print("Seeding notifications...")
        db.add_all([
            Notification(
                user_id=None,
                target_role="All",
                notification_type="System Update",
                title="Platform Maintenance Complete",
                description="Performance analytics and report generation modules upgraded successfully.",
                module_name="System",
                priority="Low",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(hours=2),
            ),
            Notification(
                user_id=None,
                target_role=Roles.PROCUREMENT_MANAGER,
                notification_type="Delivery Delay Warning",
                title="Delivery Delayed for PO-2026-0011",
                description="Cement consignment from BuildRight Materials passed its expected delivery date by 10 days.",
                module_name="Delivery",
                related_record_id="11",
                priority="High",
                delivery_method="All",
                is_read=False,
                timestamp=now - timedelta(hours=5),
            ),
            Notification(
                user_id=None,
                target_role=Roles.SUPPLY_CHAIN_MANAGER,
                notification_type="Delivery Delay Warning",
                title="Delayed Deliveries Require Review",
                description="Three purchase orders are currently tracking behind their committed delivery dates.",
                module_name="Delivery",
                priority="High",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(hours=6),
            ),
            Notification(
                user_id=None,
                target_role=Roles.PROCUREMENT_MANAGER,
                notification_type="Contract Expiry Reminder",
                title="Contract CTR-2026-0002 Expires in 22 Days",
                description="Office Supplies Master Agreement with OfficeMart Solutions expires soon. Initiate renewal.",
                module_name="Contracts",
                related_record_id="2:30",
                priority="Medium",
                delivery_method="Email",
                is_read=False,
                timestamp=now - timedelta(days=1),
            ),
            Notification(
                user_id=None,
                target_role=Roles.PROCUREMENT_MANAGER,
                notification_type="Contract Expiry Reminder",
                title="Contract CTR-2026-0004 Has Expired",
                description="Bulk Steel & Cement Supply Agreement with BuildRight Materials expired 65 days ago.",
                module_name="Contracts",
                related_record_id="4:0",
                priority="High",
                delivery_method="All",
                is_read=False,
                timestamp=now - timedelta(days=2),
            ),
            Notification(
                user_id=None,
                target_role=Roles.ADMIN,
                notification_type="Vendor Onboarding",
                title="New Vendor Registration Pending Review",
                description="GreenPack Logistics has submitted onboarding documents and requires approval.",
                module_name="Vendor",
                related_record_id="6",
                priority="Medium",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(days=2),
            ),
            Notification(
                user_id=None,
                target_role=Roles.PROCUREMENT_MANAGER,
                notification_type="Certification Expiry Reminder",
                title="Certification Expiring: ISO 9001:2015",
                description="OfficeMart Solutions' ISO 9001 certificate expires in 18 days. Request a renewed copy.",
                module_name="Compliance",
                related_record_id="3:30",
                priority="Medium",
                delivery_method="All",
                is_read=False,
                timestamp=now - timedelta(days=3),
            ),
            Notification(
                user_id=None,
                target_role=Roles.PROCUREMENT_MANAGER,
                notification_type="Compliance Alert",
                title="Compliance Issue: Environmental Compliance",
                description="BuildRight Materials is 'Non-Compliant' for Environmental Compliance. Verification required.",
                module_name="Compliance",
                related_record_id="7:0",
                priority="High",
                delivery_method="All",
                is_read=False,
                timestamp=now - timedelta(days=4),
            ),
            Notification(
                user_id=user_ids.get("rajesh@techsupply.in"),
                target_role=None,
                notification_type="Procurement Award",
                title="New Purchase Order PO-2026-0010",
                description="Purchase Order PO-2026-0010 for Server Hardware has been issued to you.",
                module_name="Procurement",
                related_record_id="10",
                priority="High",
                delivery_method="All",
                is_read=True,
                timestamp=now - timedelta(days=103),
            ),
            Notification(
                user_id=user_ids.get("kavitha@greenpack.in"),
                target_role=None,
                notification_type="Vendor Approval",
                title="Vendor Registration Under Review",
                description="Your vendor profile 'GreenPack Logistics' is awaiting approval from the procurement team.",
                module_name="Vendor",
                related_record_id="6",
                priority="Medium",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(days=2),
            ),
            Notification(
                user_id=None,
                target_role=Roles.FINANCE_OFFICER,
                notification_type="Invoice Update",
                title="Invoices Awaiting Verification",
                description="Two vendor invoices are pending finance verification before payment can be released.",
                module_name="Invoice",
                priority="Medium",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(days=1, hours=6),
            ),
            Notification(
                user_id=None,
                target_role=Roles.AUDITOR,
                notification_type="Compliance Alert",
                title="Quarterly Compliance Review Due",
                description="Compliance records for nine vendor obligations are ready for audit review.",
                module_name="Compliance",
                priority="Low",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(days=5),
            ),
            Notification(
                user_id=None,
                target_role=Roles.PROCUREMENT_MANAGER,
                notification_type="Procurement Alert",
                title="New Procurement Request PR-2026-0021",
                description="Amit Patel submitted 'Cloud Backup & DR Subscription' (IT Department) awaiting approval.",
                module_name="Procurement",
                related_record_id="21",
                priority="High",
                delivery_method="All",
                is_read=False,
                timestamp=now - timedelta(days=4),
            ),
            Notification(
                user_id=user_ids.get("vendor@vendor.com"),
                target_role=None,
                notification_type="Invoice Update",
                title="Invoice Payment Released",
                description="Payment against your most recent invoice has been approved by the finance team.",
                module_name="Invoice",
                priority="Low",
                delivery_method="In-App",
                is_read=True,
                timestamp=now - timedelta(days=20),
            ),
            Notification(
                user_id=None,
                target_role="All",
                notification_type="System Update",
                title="New Reporting Filters Available",
                description="Reports now support date range filtering and Rupee-formatted PDF exports.",
                module_name="Reports",
                priority="Low",
                delivery_method="In-App",
                is_read=False,
                timestamp=now - timedelta(days=7),
            ),
        ])

        print("Seeding activity logs...")
        activity_rows = [
            ("Admin User", "Vendor Created", "Vendor", "Vendor #2", 400, "TechSupply India Pvt Ltd onboarded"),
            ("Admin User", "Vendor Approved", "Vendor", "Vendor #2", 395, "Approval granted after document review"),
            ("Rajesh Kumar", "Document Uploaded", "Vendor", "Vendor #2", 390, "GST certificate uploaded"),
            ("Admin User", "Vendor Approved", "Vendor", "Vendor #4", 393, "CloudInfra Services approved"),
            ("Rajesh Kumar", "Procurement Request Created", "Procurement", "PR-2026-0001", 380, "IT Laptop Fleet Refresh"),
            ("Procurement Manager", "Purchase Order Generated", "Procurement", "PO-2026-0001", 378, "PO issued to TechSupply India Pvt Ltd"),
            ("Rajesh Kumar", "Invoice Uploaded", "Invoice", "INV-2026-0001", 353, "Invoice raised against PO-2026-0001"),
            ("Finance Manager", "Payment Approved", "Invoice", "INV-2026-0001", 348, "Payment released via NEFT"),
            ("Procurement Manager", "Contract Created", "Contract", "CTR-2026-0001", 120, "Annual IT hardware agreement executed"),
            ("Amit Patel", "Certification Uploaded", "Compliance", "Certification #5", 400, "ISO 27001:2022 certificate uploaded"),
            ("Supply Chain Manager", "Message Sent", "Communication", "Discussion #4", 240, "Steel consignment shortfall raised"),
            ("Suresh Reddy", "File Shared", "Communication", "File #3", 239, "Mill test certificate shared"),
            ("Procurement Manager", "Procurement Request Approved", "Procurement", "PR-2026-0009", 129, "Perimeter security upgrade approved"),
            ("Supply Chain Manager", "Delivery Status Updated", "Delivery", "PO-2026-0010", 83, "Marked as delivered"),
            ("Finance Manager", "Invoice Verified", "Invoice", "INV-2026-0008", 45, "Amounts reconciled against PO"),
            ("Auditor User", "Compliance Reviewed", "Compliance", "Compliance #7", 25, "BuildRight environmental compliance flagged"),
            ("Procurement Manager", "Vendor Assigned", "Procurement", "PR-2026-0018", 24, "Assigned to OfficeMart Solutions"),
            ("Admin User", "User Created", "User", "User #11", 400, "Vendor login provisioned for GreenPack Logistics"),
            ("Neha Kapoor", "Procurement Request Created", "Procurement", "PR-2026-0020", 9, "HR onboarding kits requested"),
            ("Amit Patel", "Procurement Request Created", "Procurement", "PR-2026-0021", 4, "Cloud backup & DR subscription requested"),
        ]
        db.add_all([
            ActivityLog(
                user_id=None,
                user_name=user_name,
                action=action,
                module_name=module,
                related_record=related,
                ip_address=f"192.168.1.{20 + index}",
                details=details,
                timestamp=now - timedelta(days=days_ago),
            )
            for index, (user_name, action, module, related, days_ago, details) in enumerate(activity_rows)
        ])

        db.commit()

        print("Recalculating vendor scores...")
        from app.services.vendor_service import update_vendor_scores
        for vid in set(vendor_ids.values()):
            try:
                update_vendor_scores(db, vid)
            except Exception as e:
                print(f"Error updating vendor {vid} scores: {e}")

        db.commit()
        print("Seed completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
