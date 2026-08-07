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
- [ ] Milestone 4 (17 Aug 2026) - Testing, deployment and documentation

## Recent updates

- 02 Aug - Refine scoring criteria in the new product evaluation screen
- 03 Aug - Round out the vendor analytics screen with category breakdown chart
- 04 Aug - Refine category breakdown chart in the vendor analytics screen
- 05 Aug - Tighten typed responses in the core API services
- 06 Aug - Create the Angular project with proxy configuration
- 07 Aug - Improve TypeScript config in the Angular project
