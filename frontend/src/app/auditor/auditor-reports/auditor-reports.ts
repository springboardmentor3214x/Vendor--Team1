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
}

const PLACEHOLDER_AUDITOR_REPORTS_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 6, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 7, name: 'Northwind Steel', status: 'Active' },
  { id: 8, name: 'Orbit IT Systems', status: 'Pending Approval' },
];

function usePlaceholderAuditorReports(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_AUDITOR_REPORTS_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
