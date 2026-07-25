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
}

const PLACEHOLDER_REPORTS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderReports(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_REPORTS_ROWS;
  }
  return rows.filter((row) => !!row);
}
