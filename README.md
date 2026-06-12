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

- 07 Jun - Add the shared dependencies with application startup
- 08 Jun - Extend the shared dependencies with CORS configuration
- 09 Jun - Refine CORS configuration in the shared dependencies
- 10 Jun - Flesh out the application config with database bootstrap
- 11 Jun - Extend the JWT handler with database bootstrap
- 12 Jun - Create the role definitions with application startup
