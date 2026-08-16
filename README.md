# Vendor Reliability Intelligence Platform

A full stack platform for evaluating vendor reliability, running procurement
operations, monitoring supplier performance and keeping contracts compliant.
It gives procurement teams a single place to register suppliers, raise and
approve purchase requests, track deliveries, score vendors on real operational
data and export the results.

Angular on the front end, FastAPI and PostgreSQL on the back end.

## Contents

- [Features](#features)
- [Architecture](#architecture)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [API overview](#api-overview)
- [Roles and permissions](#roles-and-permissions)
- [Deployment](#deployment)
- [Milestones](#milestones)
- [Team](#team)

## Features

**Authentication and role management** - registration, login, JWT sessions,
password reset, profile management and role based access control across six
roles.

**Vendor management** - vendor registration, profile and contact management,
categorisation, an approval workflow, status monitoring and document uploads.

**Procurement management** - procurement requests, purchase order creation,
multi step approvals, vendor assignment, order tracking and invoice handling.

**Vendor performance** - delivery performance monitoring, quality evaluation,
communication response tracking, service ratings, performance history and
vendor ranking.

**Vendor reliability** - a weighted reliability score per vendor, supplier
ranking, procurement risk levels, trend analysis and sourcing recommendations.

**Contracts and compliance** - a contract repository, renewal tracking,
compliance monitoring, certification management and expiry alerts.

**Communication** - vendor messaging, procurement discussions, communication
history, file sharing and activity logs.

**Dashboards and analytics** - procurement, vendor and administrator
dashboards covering spend, active orders, delivery status, performance
summaries and system statistics.

**Notifications** - procurement alerts, delivery delay warnings, approval
notifications, contract expiry reminders, email and SMS delivery.

**Reports and export** - vendor performance, procurement, purchase order,
compliance and contract reports with PDF and Excel export.

## Architecture

```
Angular client
  role based routing, guards, HTTP interceptor
        |
        |  REST over HTTP (proxied in development)
        v
FastAPI application
  api/       route handlers per module
  services/  business logic and scoring
  schemas/   request and response validation
  models/    SQLAlchemy tables
        |
        v
PostgreSQL
```

The client never talks to the database directly. Every request carries a JWT
that the backend validates before applying the role checks defined for that
endpoint.

## Repository layout

```
backend/
  app/
    api/        route handlers grouped by module
    core/       config, security, roles, dependencies, risk banding
    database/   engine, session and metadata
    models/     SQLAlchemy tables
    schemas/    Pydantic request and response models
    services/   business logic
    utils/      shared helpers
    main.py     application factory and router registration
    seed.py     demo data loader
  requirements.txt

frontend/
  src/app/
    auth/         login, registration, password reset, profile
    core/         services, guards, interceptors, shared models
    layout/       navbar, sidebar, application shell
    vendor/       vendor list, forms and details
    procurement/  requests, purchase orders, invoices, tracking
    contracts/    contract repository and compliance
    dashboard/    role based dashboards and charts
    supply-chain/ delivery performance and risk views
    vendor-portal/vendor facing screens
    admin/        user management, analytics, reports
    ui/           shared presentational components
  angular.json
  package.json
```

## Getting started

### Prerequisites

- Python 3.11 or newer
- Node.js 20 or newer
- PostgreSQL 14 or newer

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API listens on http://localhost:8000 and publishes interactive docs at
http://localhost:8000/docs.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

The dev server runs on http://localhost:4200 and proxies API paths to the
backend, so no CORS configuration is needed while developing.

### Demo data

```bash
cd backend
python -m app.seed
```

This loads sample vendors, procurement requests, purchase orders and
performance records so the dashboards have something to show.

## Configuration

Backend environment variables:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Signing key for JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Session lifetime |
| `CORS_ORIGINS` | Comma separated list of allowed origins |
| `FRONTEND_BASE_URL` | Used in notification links |
| `SEED_ON_STARTUP` | Load demo data when the app boots |

Frontend environment variables:

| Variable | Purpose |
| --- | --- |
| `BACKEND_URL` | Backend origin used by the dev proxy |

## API overview

| Prefix | Module |
| --- | --- |
| `/auth` | registration, login, password reset |
| `/users` | profile and user administration |
| `/vendors` | vendor records, approval, documents |
| `/procurements` | procurement requests and approvals |
| `/purchase-orders` | purchase orders and line items |
| `/invoices` | invoice records and payment status |
| `/order-tracking` | delivery milestones |
| `/contracts` | contracts, compliance, certifications |
| `/communication` | messages, discussions, shared files |
| `/performance` | delivery, quality and service metrics |
| `/reliability` | reliability scores and risk levels |
| `/analytics` | dashboard aggregates |
| `/notifications` | alerts and notification history |
| `/reports` | report generation and export |

## Roles and permissions

| Role | Scope |
| --- | --- |
| Administrator | full access, user management, system statistics |
| Procurement Manager | requests, purchase orders, vendor assignment |
| Supply Chain Manager | delivery performance, risk, evaluations |
| Vendor | own profile, orders, contracts and messages only |
| Finance Officer | invoices, purchase order values, cost analysis |
| Auditor | read only access to logs, compliance and reports |

Vendor accounts are scoped to their own records; the backend filters
procurements, contracts and communications by the signed in vendor rather than
relying on the client to hide data.

## Deployment

`render.yaml` describes the backend service and its PostgreSQL database.
`frontend/vercel.json` maps the API paths to the deployed backend and serves
the Angular build as a single page application. `DEPLOYMENT_GUIDE.md` walks
through both steps.

## Milestones

| Milestone | Due | Scope |
| --- | --- | --- |
| 1 | 13 Jul 2026 | Requirements, UI design, database design, backend setup |
| 2 | 24 Jul 2026 | Vendor and procurement management |
| 3 | 07 Aug 2026 | Vendor performance, reliability and analytics |
| 4 | 17 Aug 2026 | Testing, deployment and documentation |

## Team

| Member | Role |
| --- | --- |
| Harsha Vardhan Mogili | Integration and testing |
| Avinash Barla | Backend development |
| Kaustubh Thallam | Backend development |
| Alekhya Golla | Frontend development |
| Chirag | Frontend development |
