# Vendor Reliability Intelligence Platform

Full-stack web application for vendor management, procurement, and performance tracking.

## Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@vendor.com` | `Admin@123` |
| **Procurement Manager** | `procurement@vendor.com` | `Procure@123` |
| **Supply Chain Manager** | `supplychain@vendor.com` | `Supply@123` |
| **Vendor** | `vendor@vendor.com` | `Vendor@123` |
| **Finance Manager** | `finance@vendor.com` | `Finance@123` |
| **Auditor** | `auditor@vendor.com` | `Auditor@123` |

> Credentials are auto-created on first backend startup via `app/seed.py`.

## Quick Start (Local)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npx ng serve
```

- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:4200
