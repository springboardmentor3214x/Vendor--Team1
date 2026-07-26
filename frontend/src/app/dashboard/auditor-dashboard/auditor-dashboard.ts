import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';

import { ContractService } from '../../core/services/contract.service';
import { CommunicationService } from '../../core/services/communication.service';

@Component({
  selector: 'app-auditor-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
  ],
  templateUrl: './auditor-dashboard.html',
  styleUrls: ['./auditor-dashboard.css'],
})
export class AuditorDashboard implements OnInit {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Audit Activity' },
    { key: 'status', label: 'Status' }
  ];
  recentActivities: any[] = [];
  isLoading = true;
  complianceRate = 100;
  pendingAudits = 0;
  flaggedIssues = 0;
  reportsGenerated = 0;
}

const PLACEHOLDER_AUDITOR_DASHBOARD_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderAuditorDashboard(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_AUDITOR_DASHBOARD_ROWS;
  }
  return rows.filter((row) => !!row);
}
