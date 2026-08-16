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
- [x] Milestone 2 (24 Jul 2026) - Vendor and procurement management
- [x] Milestone 3 (07 Aug 2026) - Vendor performance and analytics
- [x] Milestone 4 (17 Aug 2026) - Testing, deployment and documentation

## Recent updates

- 11 Aug - Improve date filters in the performance history screen
- 12 Aug - Improve column layout in the procurement request list screen
- 13 Aug - Improve due date highlighting in the invoice management screen
- 14 Aug - Round out the navbar with logout handling
- 15 Aug - Flesh out the procurement approval screen with approve and reject actions
- 16 Aug - Improve logout handling in the navbar
