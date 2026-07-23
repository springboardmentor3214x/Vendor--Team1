import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

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
export class FinanceDashboard {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities = [
    { date: '15 Jul 2026', activity: 'Invoice INV-2024 for ₹45,000 processed', status: 'Paid' },
    { date: '14 Jul 2026', activity: 'Payment to Vendor Alpha pending approval', status: 'Pending Approval' },
    { date: '13 Jul 2026', activity: 'Quarterly tax report generated', status: 'Completed' },
    { date: '12 Jul 2026', activity: 'Budget allocation review for Q3', status: 'In Review' }
  ];

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Completed') || status.includes('Paid')) return 'success';
    if (status.includes('Pending') || status.includes('Review')) return 'warning';
    return 'default';
  }

  refresh() { alert("Data refreshed!"); }
}