from app.models.vendor import Vendor

SAMPLE_VENDORS = [
    {"name": "Northwind Steel", "category": "Raw Material Suppliers"},
    {"name": "Orbit IT Systems", "category": "IT Vendors"},
    {"name": "Delta Logistics", "category": "Logistics Partners"},
]


def load_sample_vendors(db):
    for row in SAMPLE_VENDORS:
        exists = db.query(Vendor).filter(Vendor.name == row["name"]).first()
        if exists:
            continue
        db.add(Vendor(name=row["name"], category=row["category"]))
    db.commit()
