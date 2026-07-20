import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-vendor-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './vendor-dashboard.html',
  styleUrls: ['./vendor-dashboard.css']
})
export class VendorDashboard {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities = [
    { date: '13 Jul 2026', activity: 'Vendor Profile Updated', status: 'Completed' },
    { date: '12 Jul 2026', activity: 'Invoice Uploaded', status: 'Pending Verification' },
    { date: '11 Jul 2026', activity: 'Purchase Order Received', status: 'Active' },
    { date: '10 Jul 2026', activity: 'GST Certificate Verified', status: 'Verified' }
  ];

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Completed') || status.includes('Verified')) return 'success';
    if (status.includes('Pending')) return 'warning';
    if (status.includes('Active')) return 'primary';
    return 'default';
  }

  refresh() { alert("Data refreshed!"); }
}