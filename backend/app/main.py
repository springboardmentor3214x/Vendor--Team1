from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Vendor Reliability Platform API is running!"
    }