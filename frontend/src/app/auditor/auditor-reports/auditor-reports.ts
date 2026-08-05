import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table, TableColumn } from '../../ui/table/table';
import { ReportsService, ReportFilters } from '../../core/services/reports.service';

@Component({
  selector: 'app-auditor-reports',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, Table],
  templateUrl: './auditor-reports.html',
  styleUrls: ['./auditor-reports.css']
})
export class AuditorReports implements OnInit {
  isLoading = false;
  errorMsg = '';
  selectedReportType = 'compliance';
  selectedReportTitle = 'Compliance Report';
  previewColumns: TableColumn[] = [];
  previewData: any[] = [];

  startDate = '';
  endDate = '';
  filterStatus = 'All';

  summaryCards: { label: string; value: string | number }[] = [];

  reports = [
    { type: 'compliance', title: 'Compliance Report', desc: 'Certification status, expired certifications, missing documents and vendor compliance percentage.', icon: 'verified_user' },
    { type: 'contracts', title: 'Contract Report', desc: 'Contract values, durations, responsible managers and renewal/expiry status.', icon: 'description' },
    { type: 'vendor-performance', title: 'Vendor Performance Report', desc: 'On-time delivery, quality ratings, response times and reliability scores per vendor.', icon: 'award_star' },
    { type: 'purchase-orders', title: 'Purchase Order Report', desc: 'Order values, delivery dates, statuses and invoice settlement state.', icon: 'shopping_bag' },
    { type: 'procurement-summary', title: 'Procurement Report', desc: 'Requests raised, approvals, expenditure and department-wise breakdown.', icon: 'manage_search' },
    { type: 'executive-summary', title: 'Executive Summary', desc: 'Organisation-wide totals, reliability distribution, top vendors and monthly trends.', icon: 'insights' }
  ];

  constructor(private reportsService: ReportsService) {}

  ngOnInit(): void {
    this.previewReport('compliance', 'Compliance Report');
  }

  private rupees(value: number): string {
    return `₹${(value || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }

  private currentFilters(): ReportFilters {
    return {
      startDate: this.startDate || undefined,
      endDate: this.endDate || undefined,
      status: this.filterStatus
    };
  }

  applyFilters(): void {
    this.previewReport(this.selectedReportType, this.selectedReportTitle);
  }

  resetFilters(): void {
    this.startDate = '';
    this.endDate = '';
    this.filterStatus = 'All';
    this.applyFilters();
  }

  private saveBlob(blob: Blob, fileName: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(url);
  }

  downloadPDF(): void {
    this.errorMsg = '';

    const type = this.selectedReportType === 'executive-summary' ? 'compliance' : this.selectedReportType;
    this.reportsService.downloadPDF(type, this.currentFilters()).subscribe({
      next: (blob) => this.saveBlob(blob, `${type}_report.pdf`),
      error: () => this.errorMsg = 'Failed to download the PDF report.'
    });
  }

  downloadExcel(): void {
    this.errorMsg = '';
    const type = this.selectedReportType === 'executive-summary' ? 'compliance' : this.selectedReportType;
    this.reportsService.downloadExcel(type, this.currentFilters()).subscribe({
      next: (blob) => this.saveBlob(blob, `${type}_report.xlsx`),
      error: () => this.errorMsg = 'Failed to export the Excel report.'
    });
  }

  previewReport(type: string, title: string): void {
    this.isLoading = true;
    this.errorMsg = '';
    this.selectedReportType = type;
    this.selectedReportTitle = title;
    this.summaryCards = [];

    const filters = this.currentFilters();
    const fail = () => {
      this.isLoading = false;
      this.previewData = [];
      this.errorMsg = 'Could not load the report. Please try again.';
    };

    if (type === 'compliance') {
      this.previewColumns = [
        { key: 'vendor', label: 'Vendor' },
        { key: 'complianceType', label: 'Compliance Type' },
        { key: 'status', label: 'Status' },
        { key: 'verifiedBy', label: 'Verified By' },
        { key: 'verificationDate', label: 'Verified On' },
        { key: 'expiryDate', label: 'Expires' }
      ];
      this.reportsService.getComplianceReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          const s = res?.summary || {};
          this.summaryCards = [
            { label: 'Total Records', value: s.total_records ?? 0 },
            { label: 'Compliant', value: s.compliant_count ?? 0 },
            { label: 'Non-Compliant', value: s.non_compliant_count ?? 0 },
            { label: 'Expired Certifications', value: s.expired_certifications ?? 0 },
            { label: 'Missing Documents', value: s.missing_document_vendors ?? 0 },
            { label: 'Compliance %', value: `${s.compliance_rate ?? 0}%` }
          ];
          this.previewData = (res?.items || []).map((r: any) => ({
            vendor: r.vendor_name,
            complianceType: r.compliance_type,
            status: r.status,
            verifiedBy: r.verified_by || '-',
            verificationDate: r.verification_date || '-',
            expiryDate: r.expiry_date || '-'
          }));
        },
        error: fail
      });
    } else if (type === 'contracts') {
      this.previewColumns = [
        { key: 'number', label: 'Contract #' },
        { key: 'title', label: 'Title' },
        { key: 'vendor', label: 'Vendor' },
        { key: 'value', label: 'Value' },
        { key: 'manager', label: 'Responsible Manager' },
        { key: 'status', label: 'Status' },
        { key: 'endDate', label: 'End Date' }
      ];
      this.reportsService.getContractReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.previewData = (res || []).map(c => ({
            number: c.contract_number,
            title: c.contract_title,
            vendor: c.vendor_name,
            value: this.rupees(c.contract_value),
            manager: c.responsible_manager || '-',
            status: c.status,
            endDate: c.end_date
          }));
        },
        error: fail
      });
    } else if (type === 'vendor-performance') {
      this.previewColumns = [
        { key: 'name', label: 'Vendor' },
        { key: 'category', label: 'Category' },
        { key: 'pos', label: 'POs Completed' },
        { key: 'onTime', label: 'On-Time %' },
        { key: 'delayed', label: 'Delayed' },
        { key: 'quality', label: 'Quality' },
        { key: 'reliability', label: 'Reliability' }
      ];
      this.reportsService.getVendorPerformanceReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.previewData = (res || []).map(v => ({
            name: v.company_name || v.vendor_name,
            category: v.category,
            pos: `${v.completed_pos} / ${v.total_pos}`,
            onTime: `${v.on_time_delivery_rate}%`,
            delayed: v.delayed_deliveries,
            quality: `${v.avg_quality_rating} / 5`,
            reliability: (v.reliability_score || 0).toFixed(1)
          }));
        },
        error: fail
      });
    } else if (type === 'purchase-orders') {
      this.previewColumns = [
        { key: 'poNumber', label: 'PO #' },
        { key: 'vendor', label: 'Vendor' },
        { key: 'cost', label: 'Order Value' },
        { key: 'status', label: 'Status' },
        { key: 'invoice', label: 'Invoice Status' },
        { key: 'expected', label: 'Expected Delivery' }
      ];
      this.reportsService.getPOReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.previewData = (res || []).map(po => ({
            poNumber: po.po_number,
            vendor: po.vendor_name,
            cost: this.rupees(po.total_cost),
            status: po.status,
            invoice: po.invoice_status,
            expected: po.expected_delivery_date || '-'
          }));
        },
        error: fail
      });
    } else if (type === 'procurement-summary') {
      this.previewColumns = [
        { key: 'title', label: 'Request' },
        { key: 'department', label: 'Department' },
        { key: 'total', label: 'Value' },
        { key: 'approval', label: 'Approval' },
        { key: 'status', label: 'Status' },
        { key: 'created', label: 'Created' }
      ];
      this.reportsService.getProcurementReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          const s = res?.summary || {};
          this.summaryCards = [
            { label: 'Total Requests', value: s.total_requests ?? 0 },
            { label: 'Approved', value: s.approved_requests ?? 0 },
            { label: 'Completed', value: s.completed_requests ?? 0 },
            { label: 'POs Generated', value: s.purchase_orders_generated ?? 0 },
            { label: 'Total Expenditure', value: this.rupees(s.total_expenditure) }
          ];
          this.previewData = (res?.items || []).map((p: any) => ({
            title: p.title,
            department: p.department || '-',
            total: this.rupees(p.total_price),
            approval: p.approval_status,
            status: p.status,
            created: p.created_at || '-'
          }));
        },
        error: fail
      });
    } else {

      this.previewColumns = [
        { key: 'metric', label: 'Metric' },
        { key: 'value', label: 'Value' }
      ];
      this.reportsService.getExecutiveSummaryReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          const v = res?.vendor_overview || {};
          const p = res?.procurement_overview || {};
          const c = res?.contract_overview || {};
          const comp = res?.compliance_overview || {};
          const dist = v.reliability_distribution || {};
          this.summaryCards = [
            { label: 'Total Vendors', value: v.total_vendors ?? 0 },
            { label: 'Active Vendors', value: v.active_vendors ?? 0 },
            { label: 'Total Spend', value: this.rupees(p.total_expenditure) },
            { label: 'Delayed Deliveries', value: p.delayed_deliveries ?? 0 },
            { label: 'Contracts Near Expiry', value: c.contracts_near_expiry ?? 0 },
            { label: 'Compliance %', value: `${comp.compliance_percentage ?? 0}%` }
          ];
          this.previewData = [
            { metric: 'Registered Vendors', value: v.total_vendors ?? 0 },
            { metric: 'Approved Vendors', value: v.approved_vendors ?? 0 },
            { metric: 'Low Risk Vendors', value: dist['Low Risk'] ?? 0 },
            { metric: 'Medium Risk Vendors', value: dist['Medium Risk'] ?? 0 },
            { metric: 'High Risk Vendors', value: dist['High Risk'] ?? 0 },
            { metric: 'Procurement Requests', value: p.total_requests ?? 0 },
            { metric: 'Completed Requests', value: p.completed_requests ?? 0 },
            { metric: 'Purchase Orders', value: p.total_purchase_orders ?? 0 },
            { metric: 'PO Completion Rate', value: `${p.po_completion_rate ?? 0}%` },
            { metric: 'Total Expenditure', value: this.rupees(p.total_expenditure) },
            { metric: 'Active Contracts', value: c.active_contracts ?? 0 },
            ...(v.top_vendors || []).map((t: any, i: number) => ({
              metric: `Top Vendor #${i + 1}`,
              value: `${t.company_name} (${t.reliability_score})`
            }))
          ];
        },
        error: fail
      });
    }
  }
}
