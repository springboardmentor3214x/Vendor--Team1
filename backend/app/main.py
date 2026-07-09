from app.api.user import router as user_router
from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.api.auth import router as auth_router
from app.models.vendor import Vendor
from app.api.vendor import router as vendor_router
from app.models.vendor_performance import VendorPerformance
from app.api.vendor_performance import router as performance_router
from app.models.procurement import Procurement
from app.api.procurement import router as procurement_router
from app.models.risk_assessment import RiskAssessment
from app.api.risk_assessment import router as risk_router
from app.models.purchase_order import PurchaseOrder
from app.api.purchase_order import router as purchase_order_router
from app.models.contract import Contract
from app.api.contract import router as contract_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Register the router
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vendor_router)
app.include_router(performance_router)
app.include_router(procurement_router)
app.include_router(risk_router)
app.include_router(purchase_order_router)
app.include_router(purchase_order_router)
app.include_router(contract_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Vendor Reliability Platform API is running!"
    }