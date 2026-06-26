import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import CORS_ORIGINS
from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.models.vendor import Vendor
from app.models.procurement import Procurement
from app.models.procurement_approval import ProcurementApproval
from app.models.procurement_status_history import ProcurementStatusHistory
from app.models.delivery_performance import DeliveryPerformance
from app.models.quality_evaluation import QualityEvaluation
from app.models.communication_log import CommunicationLog
from app.models.service_rating import ServiceRating
from app.models.contract import Contract
from app.models.communication import Communication
from app.models.vendor_document import VendorDocument
from app.models.purchase_order import PurchaseOrder
from app.models.order_tracking import OrderTracking
from app.models.invoice import Invoice
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.vendor import router as vendor_router
from app.api.procurement import router as procurement_router
from app.api.purchase_order import router as purchase_order_router
from app.api.order_tracking import router as order_tracking_router
from app.api.invoice import router as invoice_router
from app.api.performance import router as performance_router
from app.api.reliability import router as reliability_router
from app.api.analytics import router as analytics_router
from app.api.notification import router as notification_router
from app.api.communication import router as communication_router
from app.api.contract import router as contract_router
from app.api.reports import router as reports_router
from app.database.schema_sync import sync_schema

Base.metadata.create_all(bind=engine)

try:
    _added_columns = sync_schema(engine)
    if _added_columns:
        print(f"Schema sync added columns: {', '.join(_added_columns)}")
except Exception as e:
    print(f"Schema sync notice: {e}")

os.makedirs("static", exist_ok=True)

app = FastAPI(title="Vendor Reliability Platform API")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(vendor_router)

app.include_router(procurement_router)

app.include_router(purchase_order_router)

app.include_router(order_tracking_router)

app.include_router(invoice_router)

app.include_router(performance_router)


def _pending_main_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_main_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals


def _pending_main_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "title", "")),
            "state": getattr(item, "status", "Draft"),
            "owner": getattr(item, "created_by", None),
        })
    return rows


def _pending_main_totals_2(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
        else:
            totals["other"] = totals.get("other", 0) + 1
    return totals
