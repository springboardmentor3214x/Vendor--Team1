from fastapi import FastAPI

app = FastAPI(title="Vendor Reliability Platform API")

dummy_vendors = [{"id": 1, "name": "Acme Corp"}]

@app.get("/")
def health_check():
    return {"status": "ok", "vendors": dummy_vendors}
