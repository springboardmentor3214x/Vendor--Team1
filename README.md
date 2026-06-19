# Vendor Reliability Intelligence Platform - Backend

FastAPI service powering vendor management, procurement workflows, contract
compliance, reliability scoring, notifications and reporting.

## Tech stack

- FastAPI with Pydantic schemas
- SQLAlchemy ORM over PostgreSQL
- JWT authentication with role based access control
- ReportLab and openpyxl for PDF and Excel exports

## Getting started

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and set `DATABASE_URL` and `SECRET_KEY` before
the first run. Interactive API docs are served at http://localhost:8000/docs.

## Project layout

```
app/
  api/        route handlers grouped by module
  core/       config, security, roles, dependencies
  database/   engine, session and base metadata
  models/     SQLAlchemy tables
  schemas/    request and response models
  services/   business logic
  utils/      shared helpers
```

## Roles

Administrator, Procurement Manager, Supply Chain Manager, Vendor,
Finance Officer and Auditor, each with its own permission set.

## Milestone status

- [ ] Milestone 1 (13 Jul 2026) - Requirements, UI design, database design, backend setup
- [ ] Milestone 2 (24 Jul 2026) - Vendor and procurement management
- [ ] Milestone 3 (07 Aug 2026) - Vendor performance and analytics
- [ ] Milestone 4 (17 Aug 2026) - Testing, deployment and documentation

## Recent updates

- 14 Jun - Add password security with router registration
- 15 Jun - Round out password security with CORS configuration
- 16 Jun - Add auth schemas with account status checks
- 17 Jun - Ongoing backend work
- 18 Jun - Expand auth with account status checks
- 19 Jun - Add auth service with password reset flow
