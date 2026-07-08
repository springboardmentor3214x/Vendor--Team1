from fastapi import FastAPI
from app.database.connection import engine
from app.database.base import Base
from app.models.vendor import Vendor

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Vendor Reliability Platform API")

@app.get("/")
def health_check():
    return {"status": "ok", "database": "connected"}
