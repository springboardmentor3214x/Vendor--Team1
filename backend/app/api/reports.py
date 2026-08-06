from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import io

from app.database.connection import get_db
from app.services import report_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Reports & Export"])


@router.get("/vendor-performance")
def get_vendor_performance_report(
    category: Optional[str] = Query(None),
    min_reliability: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_vendor_performance_report(db, category=category, min_reliability=min_reliability)


@router.get("/procurement-summary")
def get_procurement_report(
    department: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_procurement_report(db, department=department, status=status)


@router.get("/purchase-orders")
def get_po_report(
    status: Optional[str] = Query(None),
    vendor_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_po_report(db, status=status, vendor_id=vendor_id)


@router.get("/compliance")
def get_compliance_report(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_compliance_report(db, status=status)


@router.get("/contracts")
def get_contract_report(
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_contract_report(db, status=status)


@router.get("/executive-summary")
def get_executive_summary_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_executive_summary_report(db)


@router.get("/export/pdf")
def export_pdf(
    report_type: str = Query("vendor-performance"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if report_type == "vendor-performance":
        data = report_service.get_vendor_performance_report(db)
        headers = ["Vendor Name", "Category", "Status", "Reliability", "Delivery", "Quality", "POs"]
        rows = [
            [v["vendor_name"], v["category"], v["approval_status"], str(v["reliability_score"]), str(v["delivery_score"]), str(v["quality_score"]), str(v["total_pos"])]
            for v in data
        ]
        title = "Vendor Performance Report"
    elif report_type == "contracts":
        data = report_service.get_contract_report(db)
        headers = ["Contract #", "Title", "Vendor", "Value", "Status", "End Date"]
        rows = [
            [c["contract_number"], c["contract_title"], c["vendor_name"], f"${c['contract_value']:,.2f}", c["status"], c["end_date"]]
            for c in data
        ]
        title = "Contract Report"
    else:
        data = report_service.get_po_report(db)
        headers = ["PO #", "Vendor", "Cost", "Status", "Expected Date"]
        rows = [
            [po["po_number"], po["vendor_name"], f"${po['total_cost']:,.2f}", po["status"], po["expected_delivery_date"]]
            for po in data
        ]
        title = "Purchase Order Report"

    pdf_bytes = report_service.generate_pdf_report(title, headers, rows)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{report_type}_report.pdf"'}
    )


@router.get("/export/excel")
def export_excel(
    report_type: str = Query("vendor-performance"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if report_type == "vendor-performance":
        data = report_service.get_vendor_performance_report(db)
        headers = ["Vendor ID", "Vendor Name", "Company", "Category", "Status", "Reliability Score", "Delivery Score", "Quality Score"]
        rows = [
            [v["vendor_id"], v["vendor_name"], v["company_name"], v["category"], v["approval_status"], v["reliability_score"], v["delivery_score"], v["quality_score"]]
            for v in data
        ]
        title = "Vendor Performance"
    elif report_type == "contracts":
        data = report_service.get_contract_report(db)
        headers = ["ID", "Contract #", "Title", "Vendor Name", "Type", "Value", "Status", "Start Date", "End Date"]
        rows = [
            [c["id"], c["contract_number"], c["contract_title"], c["vendor_name"], c["contract_type"], c["contract_value"], c["status"], c["start_date"], c["end_date"]]
            for c in data
        ]
        title = "Contracts"
    else:
        data = report_service.get_po_report(db)
        headers = ["PO ID", "PO Number", "Vendor Name", "Total Cost", "Status", "Issued Date", "Expected Delivery Date"]
        rows = [
            [po["po_id"], po["po_number"], po["vendor_name"], po["total_cost"], po["status"], po["issued_date"], po["expected_delivery_date"]]
            for po in data
        ]
        title = "Purchase Orders"

    excel_bytes = report_service.generate_excel_report(title, headers, rows)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{report_type}_report.xlsx"'}
    )
