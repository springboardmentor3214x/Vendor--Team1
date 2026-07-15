# Vendor Reliability Platform - Backend

## Module 2: Vendor Management
- POST /vendors/ — Add Vendor
- GET /vendors/ — List Vendors (pagination + filtering)
- GET /vendors/{id} — Vendor Details
- PUT /vendors/{id} — Update Vendor
- DELETE /vendors/{id} — Delete Vendor

## Module 3: Procurement Management
- POST /procurements/ — Create Procurement Request
- GET /procurements/ — List All
- GET /procurements/dashboard — Summary Dashboard
- GET /procurements/search — Search by keyword
- GET /procurements/filter — Filter by status
- GET /procurements/vendor/{id} — By Vendor
- PUT /procurements/{id} — Update
- DELETE /procurements/{id} — Delete
- POST /procurements/{id}/approve — Approve
- POST /procurements/{id}/reject — Reject
- POST /procurements/{id}/deliver — Mark Delivered
- POST /procurements/{id}/complete — Mark Completed

## Module 4: Vendor Performance Management
- GET /performance/dashboard — Performance Dashboard
- GET /performance/metrics/{vendor_id} — Weighted Metrics
- GET /performance/rankings — Vendor Rankings
- GET /performance/history/{vendor_id} — Performance History
- POST /performance/delivery — Record Delivery
- POST /performance/quality — Submit Quality Evaluation
- POST /performance/communication — Record Communication
- POST /performance/service-rating — Submit Service Rating

## Progress
- **Jul 7**: Project setup, DB, .env config. Vendor model + schemas.
- **Jul 8**: Vendor CRUD API. Module 2 complete.
- **Jul 9**: Procurement model, CRUD service, API router.
- **Jul 10**: Approval workflow, dashboard, deliver/complete. Module 3 complete.
- **Jul 13**: Performance models (4 tables), schemas, and complete service layer.
- **Jul 14**: Performance API router, weighted metrics calculation.
- **Jul 15**: Vendor rankings, performance dashboard, performance history. Module 4 complete.
