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

- [ ] Milestone 1 (13 Jul 2026) - Requirements, UI design, database design, backend setup
- [ ] Milestone 2 (24 Jul 2026) - Vendor and procurement management
- [ ] Milestone 3 (07 Aug 2026) - Vendor performance and analytics
- [ ] Milestone 4 (17 Aug 2026) - Testing, deployment and documentation

## Recent updates

- 13 Jun - Build the application shell with root routing
- 14 Jun - Smooth out the Angular project loading states found during testing
- 15 Jun - Build the application setup with router registration
- 16 Jun - Add role assignment to user
- 17 Jun - Introduce the application setup with router registration
- 18 Jun - Refine HTTP service methods in the core API services
