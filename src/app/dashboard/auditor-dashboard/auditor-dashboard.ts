import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-auditor-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './auditor-dashboard.html',
  styleUrls: ['./auditor-dashboard.css'],
})
export class AuditorDashboard {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Audit Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities = [
    { date: '15 Jul 2026', activity: 'Compliance check for Vendor Alpha', status: 'Passed' },
    { date: '14 Jul 2026', activity: 'Quarterly financial audit initiated', status: 'In Progress' },
    { date: '13 Jul 2026', activity: 'Review of PR-1022 irregularities', status: 'Flagged' },
    { date: '12 Jul 2026', activity: 'Contract renewal verification', status: 'Pending Review' }
  ];

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Passed')) return 'success';
    if (status.includes('Pending') || status.includes('Progress')) return 'warning';
    if (status.includes('Flagged')) return 'primary';
    return 'default';
  }

  refresh() { alert("Data refreshed!"); }
}