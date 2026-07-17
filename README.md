# Vendor Reliability Platform

## Overview

The Vendor Reliability Platform is a backend application developed using FastAPI and PostgreSQL. It helps organizations manage vendors, user authentication, procurement activities, vendor documents, and vendor approval workflows. The project focuses on secure authentication, role-based access control, and efficient vendor management.

---

## Tech Stack

- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Uvicorn
- Swagger UI

---

## Features

### Module 1 - User Authentication & Role Management

- User Registration
- Secure Login
- JWT Authentication
- Profile Management
- Role-Based Access Control
- Protected APIs
- Password Encryption
- Authorization using JWT Tokens

### Supported Roles

- Administrator
- Procurement Manager
- Supply Chain Manager
- Vendor
- Finance Officer
- Auditor

---

### Module 2 - Vendor Management

- Add Vendor
- View All Vendors
- Get Vendor by ID
- Update Vendor
- Delete Vendor
- Search Vendors
- Filter Vendors
- Vendor Approval
- Vendor Rejection
- Vendor Reliability Score
- Vendor Dashboard
- Vendor Pagination
- Vendor Sorting
- Vendor Document Management

---

### Module 3 - Procurement Management

- Create Procurement
- View All Procurements
- View Procurement by ID
- Update Procurement
- Delete Procurement
- Search Procurement
- Filter Procurement
- Approve Procurement
- Reject Procurement
- Procurement Dashboard
- Procurement Pagination
- Procurement Sorting

---

## Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/avinashbarla/Vendor-Reliability-Platform.git
```

### Move to Project

```bash
cd Vendor-Reliability-Platform/backend
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Configuration

Create a `.env` file.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/vendor_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run the Project

```bash
python -m uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## API Modules

### Authentication APIs

- Register User
- Login User
- Get Profile
- Update Profile

### Vendor APIs

- Add Vendor
- Get All Vendors
- Get Vendor By ID
- Update Vendor
- Delete Vendor
- Search Vendor
- Filter Vendor
- Approve Vendor
- Reject Vendor
- Upload Vendor Documents
- Vendor Dashboard
- Vendor Pagination
- Vendor Sorting

### Procurement APIs

- Add Procurement
- Get All Procurements
- Get Procurement By ID
- Update Procurement
- Delete Procurement
- Search Procurement
- Filter Procurement
- Approve Procurement
- Reject Procurement
- Procurement Dashboard
- Procurement Pagination
- Procurement Sorting

---

## Database Tables

- Users
- Vendors
- Vendor Documents
- Procurements

---

## Security

- JWT Authentication
- Password Hashing
- Role-Based Authorization
- Protected Endpoints

---

## Current Progress

- Module 1 Completed
- Module 2 Completed
- Module 3 Completed
- Purchase Order Module - In Progress
- Contract Management - Pending
- Communication Module - Pending

---

## Developed By

**Barla Avinash**

---

## Future Enhancements

- Purchase Order Management
- Contract Management
- Communication Module
- Reports & Analytics
- Notification System
- Frontend Integration (Angular)
- Deployment