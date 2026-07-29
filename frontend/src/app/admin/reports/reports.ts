import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table, TableColumn } from '../../ui/table/table';
import { ReportsService, ReportFilters } from '../../core/services/reports.service';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, Table],
  templateUrl: './reports.html',
  styleUrls: ['./reports.css']
})
export class Reports implements OnInit {
  isLoading = false;
  selectedReportType = 'vendor-performance';
  selectedReportTitle = '';
  previewData: any[] = [];
  previewColumns: TableColumn[] = [];
  errorMsg = '';

  startDate = '';
  endDate = '';
  filterCategory = 'All';
  filterStatus = 'All';
  filterDepartment = 'All';

  categories = ['All', 'IT Vendors', 'Service Providers', 'Raw Material Suppliers',
                'Logistics Partners', 'Equipment Vendors', 'Maintenance Vendors'];
  departments = ['All', 'IT Department', 'Operations', 'Logistics', 'Administration',
                 'Human Resources', 'Marketing', 'Finance'];

  reports = [
    { type: 'vendor-performance', title: 'Vendor Performance Report', desc: 'Detailed analysis of delivery accuracy, product quality, communication, and reliability scores.', icon: 'award_star' },
    { type: 'procurement-summary', title: 'Procurement Summary Log', desc: 'Detailed record of all item requests, approved budgets, status breakdowns, and vendor assignments.', icon: 'manage_search' },
    { type: 'contracts', title: 'Contract & Compliance Report', desc: 'Breakdown of active, expiring, and completed supplier contracts with financial values.', icon: 'description' },
    { type: 'purchase-orders', title: 'Purchase Orders & Fulfilment', desc: 'Compilation of purchase order statuses, issued costs, and delivery date performance.', icon: 'shopping_bag' }
  ];

  constructor(private reportsService: ReportsService) {}

  ngOnInit(): void {
    this.previewReport('vendor-performance', 'Vendor Performance Report');
  }

  private rupees(value: number): string {
    return `₹${(value || 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }

  private currentFilters(): ReportFilters {
    return {
      startDate: this.startDate || undefined,
      endDate: this.endDate || undefined,
      category: this.filterCategory,
      status: this.filterStatus,
      department: this.filterDepartment
    };
  }

  applyFilters(): void {
    this.previewReport(this.selectedReportType, this.selectedReportTitle);
  }

  resetFilters(): void {
    this.startDate = '';
    this.endDate = '';
    this.filterCategory = 'All';
    this.filterStatus = 'All';
    this.filterDepartment = 'All';
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

  downloadPDF(reportType: string = this.selectedReportType): void {
    this.errorMsg = '';
    this.reportsService.downloadPDF(reportType, this.currentFilters()).subscribe({
      next: (blob) => this.saveBlob(blob, `${reportType}_report.pdf`),
      error: () => this.errorMsg = 'Failed to download the PDF report.'
    });
  }

  downloadCSV(reportType: string = this.selectedReportType): void {
    this.errorMsg = '';
    this.reportsService.downloadExcel(reportType, this.currentFilters()).subscribe({
      next: (blob) => this.saveBlob(blob, `${reportType}_report.xlsx`),
      error: () => this.errorMsg = 'Failed to export the Excel report.'
    });
  }

  exportAll(): void {
    this.downloadPDF('vendor-performance');
    setTimeout(() => this.downloadCSV('contracts'), 500);
    setTimeout(() => this.downloadCSV('purchase-orders'), 1000);
  }

  previewReport(type: string, title: string): void {
    this.isLoading = true;
    this.errorMsg = '';
    this.selectedReportType = type;
    this.selectedReportTitle = title;

    const filters = this.currentFilters();
    const fail = () => {
      this.isLoading = false;
      this.previewData = [];
      this.errorMsg = 'Could not load the report. Please try again.';
    };

    if (type === 'vendor-performance') {
      this.previewColumns = [
        { key: 'name', label: 'Vendor Name' },
        { key: 'category', label: 'Category' },
        { key: 'totalPOs', label: 'POs Completed' },
        { key: 'onTime', label: 'On-Time %' },
        { key: 'delayed', label: 'Delayed' },
        { key: 'quality', label: 'Quality Rating' },
        { key: 'response', label: 'Response (hrs)' },
        { key: 'service', label: 'Service Rating' },
        { key: 'reliability', label: 'Reliability Score' }
      ];
      this.reportsService.getVendorPerformanceReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.previewData = (res || []).map(v => ({
            name: v.company_name || v.vendor_name,
            category: v.category,
            totalPOs: `${v.completed_pos} / ${v.total_pos}`,
            onTime: `${v.on_time_delivery_rate}%`,
            delayed: v.delayed_deliveries,
            quality: `${v.avg_quality_rating} / 5`,
            response: v.avg_response_hours,
            service: `${v.avg_service_rating} / 5`,
            reliability: (v.reliability_score || 0).toFixed(1)
          }));
        },
        error: fail
      });
    } else if (type === 'contracts') {
      this.previewColumns = [
        { key: 'number', label: 'Contract #' },
        { key: 'title', label: 'Title' },
        { key: 'vendor', label: 'Vendor' },
        { key: 'value', label: 'Contract Value' },
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
    } else if (type === 'purchase-orders') {
      this.previewColumns = [
        { key: 'poNumber', label: 'PO #' },
        { key: 'vendor', label: 'Vendor' },
        { key: 'item', label: 'Item' },
        { key: 'cost', label: 'Order Value' },
        { key: 'status', label: 'Status' },
        { key: 'invoice', label: 'Invoice Status' },
        { key: 'date', label: 'Expected Delivery' }
      ];
      this.reportsService.getPOReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          this.previewData = (res || []).map(po => ({
            poNumber: po.po_number,
            vendor: po.vendor_name,
            item: po.item_name,
            cost: this.rupees(po.total_cost),
            status: po.status,
            invoice: po.invoice_status,
            date: po.expected_delivery_date || 'N/A'
          }));
        },
        error: fail
      });
    } else {
      this.previewColumns = [
        { key: 'title', label: 'Request Title' },
        { key: 'department', label: 'Department' },
        { key: 'category', label: 'Category' },
        { key: 'total', label: 'Total Amount' },
        { key: 'approval', label: 'Approval' },
        { key: 'status', label: 'Status' },
        { key: 'created', label: 'Created' }
      ];
      this.reportsService.getProcurementReport(filters).subscribe({
        next: (res) => {
          this.isLoading = false;
          const items = Array.isArray(res) ? res : (res?.items || []);
          this.previewData = items.map((p: any) => ({
            title: p.title || p.item_name || 'Procurement Item',
            department: p.department || '-',
            category: p.category || 'General',
            total: this.rupees(p.total_price || p.total_cost),
            approval: p.approval_status || '-',
            status: p.status || '-',
            created: p.created_at || '-'
          }));
        },
        error: fail
      });
    }
  }
}
