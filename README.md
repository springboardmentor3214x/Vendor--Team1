# Vendor Reliability Intelligence Platform

Full stack platform for evaluating vendor reliability, running procurement
operations, monitoring supplier performance and keeping contracts compliant.
An Angular front end talks to a FastAPI backend backed by PostgreSQL.

## Repository layout

```
backend/   FastAPI service, SQLAlchemy models, business logic
frontend/  Angular client, dashboards and role based views
```

## Running locally

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm start
```

## Integration notes

The Angular dev server proxies API traffic to the backend, so both halves can
run side by side without CORS changes. Role based routing on the client mirrors
the permission checks enforced on every endpoint.

## Milestone status

- [x] Milestone 1 (13 Jul 2026) - Requirements, UI design, database design, backend setup
- [ ] Milestone 2 (24 Jul 2026) - Vendor and procurement management
- [ ] Milestone 3 (07 Aug 2026) - Vendor performance and analytics
- [ ] Milestone 4 (17 Aug 2026) - Testing, deployment and documentation

## Recent updates

- 13 Jul - Round out the order tracking screen with status updates
- 14 Jul - Round out the vendor assignment screen with reliability hints
- 15 Jul - Rework certification expiry in the compliance management screen
- 16 Jul - Expand contract with compliance clauses
- 17 Jul - Rework issuing authority details in certification
- 18 Jul - Handle empty responses from the auditor dashboard screen in the integrated flow
