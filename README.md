# Vendor Reliability Platform - Integrated Build

## Project Structure
```
Vendor--Team1/
├── backend/         # FastAPI Backend (Python)
│   ├── app/
│   │   ├── api/             # API route handlers
│   │   ├── database/        # SQLAlchemy connection & base
│   │   ├── models/          # ORM models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── main.py          # App entry point (CORS enabled)
│   └── requirements.txt
│
├── frontend/        # Angular Frontend (TypeScript)
│   ├── src/
│   │   ├── app/             # Angular components & services
│   │   ├── environments/    # API URL configuration
│   │   └── index.html
│   ├── angular.json
│   └── package.json
│
└── README.md
```

## How to Run

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend runs at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### Frontend (Angular)
```bash
cd frontend
npm install
ng serve
```
Frontend runs at: **http://localhost:4200**

## Modules Implemented

### Backend APIs
- **Module 2**: Vendor Management (CRUD, pagination, filtering)
- **Module 3**: Procurement Management (CRUD, approval workflow, order lifecycle, dashboard)
- **Module 4**: Vendor Performance (delivery, quality, communication, service rating, metrics, rankings)

### Frontend Pages
- Login, Registration, Forgot Password, Profile
- Role-based Dashboards (Admin, Procurement Manager, Supply Chain Manager, Vendor, Finance, Auditor)
- Vendor Management (List, Add, Edit, Details, Approval, Status Monitoring)
- Procurement (Requests, Approval, Purchase Orders, Order Tracking, Invoice Management)
- Vendor Performance (Delivery, Quality, Communication, Service Rating, History, Rankings)

## Integration Details
- Backend CORS is configured to accept requests from `http://localhost:4200`
- Frontend environment config points to `http://localhost:8000`
- Angular `HttpClient` is provisioned in app config for API communication
