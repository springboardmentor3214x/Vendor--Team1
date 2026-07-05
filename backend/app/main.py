from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base
from app.models.user import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Vendor Reliability Platform API is running!"
    }