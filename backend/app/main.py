from app.api.user import router as user_router
from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.api.auth import router as auth_router

app = FastAPI()

# Register the router
app.include_router(user_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Vendor Reliability Platform API is running!"
    }