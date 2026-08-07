from app.database.connection import engine, SessionLocal
from app.database.base import Base
from app.core.security import hash_password
from app.models.user import User
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.models.contract import Contract
from app.models.communication import Communication
from datetime import datetime, timedelta, date
from app.utils.delivery_timing import delivery_status_from_times


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

from app.core.roles import Roles

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
]

DEFAULT_VENDORS = [
    {
        "vendor_name": "Vendor User",
        "company_name": "Global Vendor Solutions",
        "email": "vendor@vendor.com",
        "phone": "9876543213",
        "address": "Cyber City, Gurgaon, Haryana",
        "category": "IT Vendors",
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
        "address": "Sector 62, Noida, Uttar Pradesh",
        "category": "IT Vendors",
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
        "address": "MG Road, Bangalore, Karnataka",
        "category": "Service Providers",
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
        "address": "HITEC City, Hyderabad, Telangana",
        "category": "Service Providers",
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
        "address": "Jubilee Hills, Hyderabad, Telangana",
        "category": "Raw Material Suppliers",
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
        "address": "Kochi, Kerala",
        "category": "Logistics Partners",
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

DEFAULT_VENDOR_USERS = [
    {
        "name": vendor["vendor_name"],
        "email": vendor["email"],
        "mobile_number": vendor["phone"],
        "password": "Vendor@123",
        "role": Roles.VENDOR,
    }
    for vendor in DEFAULT_VENDORS
]

def seed_database(reset: bool = True):
    if reset:
        Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seen_emails = set()
        for u in [*DEFAULT_USERS, *DEFAULT_VENDOR_USERS]:
            if u["email"] in seen_emails:
                continue
            seen_emails.add(u["email"])
            existing = db.query(User).filter(User.email == u["email"]).first()
            if existing:
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

        vendor_ids = {}
        for v in DEFAULT_VENDORS:
            existing_v = db.query(Vendor).filter(Vendor.company_name == v["company_name"]).first()
            if existing_v:
                vendor_ids[v["company_name"]] = existing_v.id
            else:
                vendor = Vendor(**v)
                db.add(vendor)
                db.flush()
                vendor_ids[v["company_name"]] = vendor.id

        # Seed Procurements
        print("Seeding procurements...")
        now = datetime.utcnow()
        procurements = [
            Procurement(
                item_name="Dell Laptops (Latitude 5540)",
                vendor_id=vendor_ids.get("TechSupply India Pvt Ltd", 1),
                quantity=25,
                unit_price=72000.00,
                total_price=1800000.00,
                status="Delivered",
                approval_status="Approved",
                approved_by="Procurement Manager",
                expected_delivery_date=now - timedelta(days=10),
                actual_delivery_date=now - timedelta(days=8),
                created_at=now - timedelta(days=30),
            ),
            Procurement(
                item_name="Office Chairs (Ergonomic)",
                vendor_id=vendor_ids.get("OfficeMart Solutions", 2),
                quantity=50,
                unit_price=8500.00,
                total_price=425000.00,
                status="Delivered",
                approval_status="Approved",
                approved_by="Procurement Manager",
                expected_delivery_date=now - timedelta(days=15),
                actual_delivery_date=now - timedelta(days=12),
                created_at=now - timedelta(days=25),
            ),
            Procurement(
                item_name="AWS Cloud Credits (Annual)",
                vendor_id=vendor_ids.get("CloudInfra Services", 3),
                quantity=1,
                unit_price=500000.00,
                total_price=500000.00,
                status="Completed",
                approval_status="Approved",
                approved_by="Admin User",
                expected_delivery_date=now - timedelta(days=5),
                actual_delivery_date=now - timedelta(days=5),
                created_at=now - timedelta(days=20),
            ),
            Procurement(
                item_name="Steel Rods (TMT 500D)",
                vendor_id=vendor_ids.get("BuildRight Materials", 4),
                quantity=200,
                unit_price=4500.00,
                total_price=900000.00,
                status="Ordered",
                approval_status="Approved",
                approved_by="Procurement Manager",
                expected_delivery_date=now + timedelta(days=5),
                actual_delivery_date=None,
                created_at=now - timedelta(days=10),
            ),
            Procurement(
                item_name="Networking Switches (Cisco)",
                vendor_id=vendor_ids.get("TechSupply India Pvt Ltd", 1),
                quantity=10,
                unit_price=35000.00,
                total_price=350000.00,
                status="Pending",
                approval_status="Pending",
                approved_by=None,
                expected_delivery_date=now + timedelta(days=15),
                actual_delivery_date=None,
                created_at=now - timedelta(days=3),
            ),
            Procurement(
                item_name="Printer Paper (A4, 5000 sheets)",
                vendor_id=vendor_ids.get("OfficeMart Solutions", 2),
                quantity=100,
                unit_price=350.00,
                total_price=35000.00,
                status="Ordered",
                approval_status="Approved",
                approved_by="Procurement Manager",
                expected_delivery_date=now + timedelta(days=3),
                actual_delivery_date=None,
                created_at=now - timedelta(days=5),
            ),
            Procurement(
                item_name="Azure DevOps Licenses",
                vendor_id=vendor_ids.get("CloudInfra Services", 3),
                quantity=30,
                unit_price=12000.00,
                total_price=360000.00,
                status="Pending",
                approval_status="Pending",
                approved_by=None,
                expected_delivery_date=now + timedelta(days=10),
                actual_delivery_date=None,
                created_at=now - timedelta(days=1),
            ),
            Procurement(
                item_name="Cement Bags (OPC 53 Grade)",
                vendor_id=vendor_ids.get("BuildRight Materials", 4),
                quantity=500,
                unit_price=380.00,
                total_price=190000.00,
                status="Cancelled",
                approval_status="Rejected",
                approved_by="Admin User",
                expected_delivery_date=now + timedelta(days=7),
                actual_delivery_date=None,
                created_at=now - timedelta(days=8),
            ),
        ]
        db.add_all(procurements)
        db.flush()

        # Seed Delivery Performances
        print("Seeding delivery performance...")
        delivery_records = [
            _delivery_row(
                vendor_ids.get("TechSupply India Pvt Ltd", 1),
                procurements[0].id,
                now - timedelta(days=10),
                now - timedelta(days=10, hours=2),
                "Laptops reached warehouse slightly after slot",
            ),
            _delivery_row(
                vendor_ids.get("OfficeMart Solutions", 2),
                procurements[1].id,
                now - timedelta(days=15, hours=10),
                now - timedelta(days=15, hours=7),
                "Chairs delivered within 3 hour window",
            ),
            _delivery_row(
                vendor_ids.get("CloudInfra Services", 3),
                procurements[2].id,
                now - timedelta(days=5, hours=14),
                now - timedelta(days=5, hours=13, minutes=20),
                "Credits activated before deadline",
            ),
        ]
        db.add_all(delivery_records)

        # Seed Quality Evaluations
        print("Seeding quality evaluations...")
        quality_records = [
            QualityEvaluation(
                vendor_id=vendor_ids.get("TechSupply India Pvt Ltd", 1),
                procurement_id=procurements[0].id,
                material_quality=5,
                packaging_quality=4,
                quantity_accuracy=5,
                specification_compliance=4,
                defect_count=1,
                overall_rating=4.5,
                remarks="All laptops working, 1 had minor scratch on casing",
            ),
            QualityEvaluation(
                vendor_id=vendor_ids.get("OfficeMart Solutions", 2),
                procurement_id=procurements[1].id,
                material_quality=4,
                packaging_quality=3,
                quantity_accuracy=5,
                specification_compliance=4,
                defect_count=2,
                overall_rating=3.8,
                remarks="2 chairs had wobbly armrests, replaced promptly",
            ),
            QualityEvaluation(
                vendor_id=vendor_ids.get("CloudInfra Services", 3),
                procurement_id=procurements[2].id,
                material_quality=5,
                packaging_quality=5,
                quantity_accuracy=5,
                specification_compliance=5,
                defect_count=0,
                overall_rating=5.0,
                remarks="Perfect service, all credits activated correctly",
            ),
        ]
        db.add_all(quality_records)

        # Seed Communication Logs (aggregates response duration)
        print("Seeding communication logs...")
        comm_logs = [
            CommunicationLog(
                vendor_id=vendor_ids.get("TechSupply India Pvt Ltd", 1),
                procurement_id=procurements[0].id,
                message_sent_time=now - timedelta(days=12),
                vendor_response_time=now - timedelta(days=12, hours=-2),
                response_duration_hours=2.0,
                communication_status="Responded",
                remarks="Quick response on delivery schedule update",
            ),
            CommunicationLog(
                vendor_id=vendor_ids.get("OfficeMart Solutions", 2),
                procurement_id=procurements[1].id,
                message_sent_time=now - timedelta(days=18),
                vendor_response_time=now - timedelta(days=18, hours=-6),
                response_duration_hours=6.0,
                communication_status="Responded",
                remarks="Invoice sent after reminder",
            ),
            CommunicationLog(
                vendor_id=vendor_ids.get("CloudInfra Services", 3),
                procurement_id=procurements[2].id,
                message_sent_time=now - timedelta(days=6),
                vendor_response_time=now - timedelta(days=6, hours=-1),
                response_duration_hours=1.0,
                communication_status="Responded",
                remarks="Immediate confirmation of license activation",
            ),
        ]
        db.add_all(comm_logs)

        # Seed Service Ratings
        print("Seeding service ratings...")
        service_records = [
            ServiceRating(
                vendor_id=vendor_ids.get("TechSupply India Pvt Ltd", 1),
                procurement_id=procurements[0].id,
                professionalism=4,
                customer_support=4,
                documentation_quality=5,
                flexibility=4,
                communication_effectiveness=4,
                issue_resolution=4,
                overall_rating=4.2,
                comments="Reliable IT equipment vendor, good pricing",
            ),
            ServiceRating(
                vendor_id=vendor_ids.get("OfficeMart Solutions", 2),
                procurement_id=procurements[1].id,
                professionalism=4,
                customer_support=3,
                documentation_quality=4,
                flexibility=4,
                communication_effectiveness=3,
                issue_resolution=4,
                overall_rating=3.7,
                comments="Decent quality, communication could be faster",
            ),
            ServiceRating(
                vendor_id=vendor_ids.get("CloudInfra Services", 3),
                procurement_id=procurements[2].id,
                professionalism=5,
                customer_support=5,
                documentation_quality=5,
                flexibility=4,
                communication_effectiveness=5,
                issue_resolution=5,
                overall_rating=4.8,
                comments="Outstanding cloud services, highly recommended",
            ),
        ]
        db.add_all(service_records)

        # Seed Contracts
        print("Seeding contracts...")
        today_val = date.today()
        contracts = [
            Contract(
                contract_title="Annual IT HW Maintenance & Licensing Agreement",
                vendor_id=vendor_ids.get("TechSupply India Pvt Ltd", 1),
                vendor_name="TechSupply India Pvt Ltd",
                start_date=today_val - timedelta(days=120),
                end_date=today_val + timedelta(days=245),
                contract_value=1200000.0,
                status="Active",
            ),
            Contract(
                contract_title="Office Supplies Master Agreement - v2",
                vendor_id=vendor_ids.get("OfficeMart Solutions", 2),
                vendor_name="OfficeMart Solutions",
                start_date=today_val - timedelta(days=30),
                end_date=today_val + timedelta(days=335),
                contract_value=450000.0,
                status="Active",
            ),
            Contract(
                contract_title="AWS Multi-Account Support & Optimization SLA",
                vendor_id=vendor_ids.get("CloudInfra Services", 3),
                vendor_name="CloudInfra Services",
                start_date=today_val - timedelta(days=90),
                end_date=today_val + timedelta(days=275),
                contract_value=2400000.0,
                status="Active",
            ),
        ]
        db.add_all(contracts)

        # Seed Communications (discussion chats)
        print("Seeding communications...")
        comms = [
            Communication(
                procurement_id=procurements[0].id,
                sender="Procurement Manager",
                message="Hi Rajesh, could you provide a tracking update for the Dell Latitude laptops?",
                sent_at=now - timedelta(days=12),
            ),
            Communication(
                procurement_id=procurements[0].id,
                sender="Rajesh Kumar",
                message="Hello, the dispatch details have been updated. They should arrive tomorrow morning.",
                sent_at=now - timedelta(days=12, hours=-2),
            ),
            Communication(
                procurement_id=procurements[1].id,
                sender="Procurement Manager",
                message="Priya, we received the chairs but 2 have minor armrest stability issues.",
                sent_at=now - timedelta(days=15),
            ),
            Communication(
                procurement_id=procurements[1].id,
                sender="Priya Sharma",
                message="Apologies for that. We'll send a service technician tomorrow to replace or fix them.",
                sent_at=now - timedelta(days=14),
            ),
        ]
        db.add_all(comms)

        db.commit()

        # Update vendor denormalized performance scores
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
    seed_database(reset=True)
