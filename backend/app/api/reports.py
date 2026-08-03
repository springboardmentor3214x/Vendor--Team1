from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import io

from app.database.connection import get_db
from app.services import report_service
from app.services.report_service import format_currency, describe_filters
from app.core.dependencies import get_current_user, role_required
from app.core.roles import INTERNAL_ROLES
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports & Export"])


@router.get("/vendor-performance")
def get_vendor_performance_report(
    category: Optional[str] = Query(None),
    min_reliability: Optional[float] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return report_service.get_vendor_performance_report(
        db, category=category, min_reliability=min_reliability,
        start_date=start_date, end_date=end_date
    )


@router.get("/procurement-summary")
def get_procurement_report(
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return report_service.get_procurement_report(
        db, department=department, status=status,
        start_date=start_date, end_date=end_date
    )


@router.get("/purchase-orders")
def get_po_report(
    status: Optional[str] = Query(None),
    vendor_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return report_service.get_po_report(
        db, status=status, vendor_id=vendor_id,
        start_date=start_date, end_date=end_date
    )


@router.get("/compliance")
def get_compliance_report(
    status: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return report_service.get_compliance_report(
        db, status=status, start_date=start_date, end_date=end_date
    )


@router.get("/contracts")
def get_contract_report(
    status: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    expiring_within_days: Optional[int] = Query(None, description="Only contracts expiring within N days (30/60/90)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return report_service.get_contract_report(
        db, status=status, start_date=start_date, end_date=end_date,
        expiring_within_days=expiring_within_days
    )


@router.get("/executive-summary")
def get_executive_summary_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    return report_service.get_executive_summary_report(db, start_date=start_date, end_date=end_date)


def _build_report_payload(db: Session, report_type: str, filters: dict, for_excel: bool):
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    status = filters.get("status")
    category = filters.get("category")
    vendor_id = filters.get("vendor_id")
    department = filters.get("department")

    if report_type == "vendor-performance":
        data = report_service.get_vendor_performance_report(
            db, category=category, start_date=start_date, end_date=end_date
        )
        if for_excel:
            headers = ["Vendor ID", "Vendor Name", "Company", "Category", "Approval Status",
                       "Total POs", "Completed POs", "On-Time Delivery %", "Delayed Deliveries",
                       "Avg Quality Rating", "Avg Response (hrs)", "Avg Service Rating",
                       "Reliability Score", "Delivery Score", "Quality Score"]
            rows = [
                [v["vendor_id"], v["vendor_name"], v["company_name"], v["category"], v["approval_status"],
                 v["total_pos"], v["completed_pos"], v["on_time_delivery_rate"], v["delayed_deliveries"],
                 v["avg_quality_rating"], v["avg_response_hours"], v["avg_service_rating"],
                 v["reliability_score"], v["delivery_score"], v["quality_score"]]
                for v in data
            ]
        else:
            headers = ["Vendor", "Category", "POs", "On-Time %", "Delayed", "Quality", "Response (h)", "Reliability"]
            rows = [
                [v["company_name"], v["category"], str(v["total_pos"]), f"{v['on_time_delivery_rate']}%",
                 str(v["delayed_deliveries"]), str(v["avg_quality_rating"]),
                 str(v["avg_response_hours"]), str(v["reliability_score"])]
                for v in data
            ]
        return "Vendor Performance Report", headers, rows

    if report_type == "contracts":
        data = report_service.get_contract_report(db, status=status, start_date=start_date, end_date=end_date)
        if for_excel:
            headers = ["ID", "Contract #", "Title", "Vendor Name", "Type", "Value (INR)",
                       "Payment Terms", "Responsible Manager", "Status", "Start Date", "End Date", "Days to Expiry"]
            rows = [
                [c["id"], c["contract_number"], c["contract_title"], c["vendor_name"], c["contract_type"],
                 c["contract_value"], c["payment_terms"], c["responsible_manager"], c["status"],
                 c["start_date"], c["end_date"], c["days_to_expiry"]]
                for c in data
            ]
        else:
            headers = ["Contract #", "Title", "Vendor", "Value", "Status", "End Date"]
            rows = [
                [c["contract_number"], c["contract_title"], c["vendor_name"],
                 format_currency(c["contract_value"]), c["status"], c["end_date"]]
                for c in data
            ]
        return "Contract Report", headers, rows

    if report_type == "compliance":
        data = report_service.get_compliance_report(db, status=status, start_date=start_date, end_date=end_date)
        headers = ["Vendor", "Compliance Type", "Status", "Verified By", "Verification Date", "Expiry Date"]
        rows = [
            [r["vendor_name"], r["compliance_type"], r["status"], r["verified_by"] or "-",
             r["verification_date"] or "-", r["expiry_date"] or "-"]
            for r in data["items"]
        ]
        return "Compliance Report", headers, rows

    if report_type == "procurement-summary":
        data = report_service.get_procurement_report(
            db, department=department, status=status, start_date=start_date, end_date=end_date
        )
        if for_excel:
            headers = ["ID", "Title", "Department", "Category", "Quantity", "Total Price (INR)",
                       "Approval Status", "Status", "Created Date"]
            rows = [
                [r["id"], r["title"], r["department"], r["category"], r["quantity"],
                 r["total_price"], r["approval_status"], r["status"], r["created_at"]]
                for r in data["items"]
            ]
        else:
            headers = ["Title", "Department", "Qty", "Value", "Approval", "Status", "Created"]
            rows = [
                [r["title"], r["department"], str(r["quantity"]), format_currency(r["total_price"]),
                 r["approval_status"], r["status"], r["created_at"]]
                for r in data["items"]
            ]
        return "Procurement Summary Report", headers, rows

    data = report_service.get_po_report(
        db, status=status, vendor_id=vendor_id, start_date=start_date, end_date=end_date
    )
    if for_excel:
        headers = ["PO ID", "PO Number", "Vendor Name", "Item", "Total Cost (INR)", "Tax (INR)",
                   "Status", "Invoice Status", "PO Date", "Expected Delivery", "Actual Delivery"]
        rows = [
            [po["po_id"], po["po_number"], po["vendor_name"], po["item_name"], po["total_cost"],
             po["tax_amount"], po["status"], po["invoice_status"], po["issued_date"],
             po["expected_delivery_date"], po["actual_delivery_date"]]
            for po in data
        ]
    else:
        headers = ["PO #", "Vendor", "Cost", "Status", "Invoice", "Expected Date"]
        rows = [
            [po["po_number"], po["vendor_name"], format_currency(po["total_cost"]),
             po["status"], po["invoice_status"], po["expected_delivery_date"]]
            for po in data
        ]
    return "Purchase Order Report", headers, rows


@router.get("/export/pdf")
def export_pdf(
    report_type: str = Query("vendor-performance"),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    vendor_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    filters = {
        "status": status, "category": category, "department": department,
        "vendor_id": vendor_id, "start_date": start_date, "end_date": end_date
    }
    title, headers, rows = _build_report_payload(db, report_type, filters, for_excel=False)

    pdf_bytes = report_service.generate_pdf_report(
        title, headers, rows, applied_filters=describe_filters(**filters)
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{report_type}_report.pdf"'}
    )


@router.get("/export/excel")
def export_excel(
    report_type: str = Query("vendor-performance"),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    vendor_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(INTERNAL_ROLES))
):
    filters = {
        "status": status, "category": category, "department": department,
        "vendor_id": vendor_id, "start_date": start_date, "end_date": end_date
    }
    title, headers, rows = _build_report_payload(db, report_type, filters, for_excel=True)

    excel_bytes = report_service.generate_excel_report(title, headers, rows)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{report_type}_report.xlsx"'}
    )
