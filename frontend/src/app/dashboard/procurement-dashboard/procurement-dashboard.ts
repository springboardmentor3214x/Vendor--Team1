import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-procurement-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './procurement-dashboard.html',
  styleUrls: ['./procurement-dashboard.css'],
})
export class ProcurementDashboard {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities = [
    { date: '15 Jul 2026', activity: 'New Request PR-1024 created', status: 'Pending Approval' },
    { date: '14 Jul 2026', activity: 'Purchase Order PO-998 dispatched', status: 'In Transit' },
    { date: '13 Jul 2026', activity: 'Vendor TechCorp approved', status: 'Completed' },
    { date: '12 Jul 2026', activity: 'RFP evaluation for office supplies', status: 'In Progress' }
  ];

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Completed')) return 'success';
    if (status.includes('Pending') || status.includes('Progress')) return 'warning';
    if (status.includes('Transit')) return 'primary';
    return 'default';
  }

  refresh() { alert("Data refreshed!"); }
}