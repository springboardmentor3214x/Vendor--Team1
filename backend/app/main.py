from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.database.connection import engine
from app.database.base import Base

from app.models.user import User
from app.models.vendor import Vendor
from app.models.procurement import Procurement
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
from app.api.communication import router as communication_router
from app.api.contract import router as contract_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vendor Reliability Platform API")

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
app.include_router(contract_router)
app.include_router(communication_router)


@app.on_event("startup")
def on_startup():
    from app.seed import seed_database
    try:
        seed_database()
    except Exception as e:
        print(f"Seed warning: {e}")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Vendor Reliability Platform API is running"}
