import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';

import { InvoiceService } from '../../core/services/invoice.service';
import { CommunicationService } from '../../core/services/communication.service';

@Component({
  selector: 'app-finance-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
  ],
  templateUrl: './finance-dashboard.html',
  styleUrls: ['./finance-dashboard.css'],
})
export class FinanceDashboard implements OnInit {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];
  recentActivities: any[] = [];
  isLoading = true;
  pendingPaymentsCount = 0;
}

const PLACEHOLDER_FINANCE_DASHBOARD_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderFinanceDashboard(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_FINANCE_DASHBOARD_ROWS;
}
