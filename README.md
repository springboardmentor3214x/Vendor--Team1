# Vendor Reliability Intelligence Platform - Frontend

Angular client for the Vendor Reliability Intelligence and Procurement Risk
Management Platform. It covers vendor onboarding, procurement workflows,
contract tracking, performance dashboards and reporting for six user roles.

## Tech stack

- Angular with standalone components
- Angular Material and Bootstrap for layout
- RxJS for state and HTTP composition
- Chart.js for dashboard visualisations

## Getting started

```bash
cd frontend
npm install
npm start
```

The dev server runs on http://localhost:4200 and proxies API calls to the
FastAPI backend. Copy `.env.example` to `.env` and set `BACKEND_URL` before
starting if the backend is not on the default port.

## Project layout

```
src/app/
  auth/         login, registration, password reset, profile
  core/         services, guards, interceptors, shared models
  layout/       navbar, sidebar, shell
  vendor/       vendor list, forms, details
  procurement/  requests, purchase orders, invoices, tracking
  contracts/    contract repository and compliance
  dashboard/    role based dashboards and charts
  supply-chain/ delivery performance and risk views
  admin/        user management, analytics, reports
  ui/           shared presentational components
```

## Milestone status

- [x] Milestone 1 (13 Jul 2026) - Requirements, UI design, database design, backend setup
- [ ] Milestone 2 (24 Jul 2026) - Vendor and procurement management
- [ ] Milestone 3 (07 Aug 2026) - Vendor performance and analytics
- [ ] Milestone 4 (17 Aug 2026) - Testing, deployment and documentation

## Recent updates

- 02 Jul - Create the search component with clear control
- 03 Jul - Create the table component with empty states
- 04 Jul - Add the compliance management screen with certification expiry
- 05 Jul - Add the contract details screen with attached documents
- 06 Jul - Extend the core API services with HTTP service methods
- 07 Jul - Expand the button component with disabled styling
