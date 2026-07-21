import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-supply-chain-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './supply-chain-dashboard.html',
  styleUrls: ['./supply-chain-dashboard.css'],
})
export class SupplyChainDashboard {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities = [
    { date: '15 Jul 2026', activity: 'Shipment SHP-8890 arrived at warehouse', status: 'Delivered' },
    { date: '14 Jul 2026', activity: 'Quality check for Raw Materials', status: 'In Progress' },
    { date: '13 Jul 2026', activity: 'Inventory level critical for Item X', status: 'Warning' },
    { date: '12 Jul 2026', activity: 'Logistics contract renewed', status: 'Completed' }
  ];

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Completed') || status.includes('Delivered')) return 'success';
    if (status.includes('Warning') || status.includes('Progress')) return 'warning';
    return 'default';
  }

  refresh() { alert("Data refreshed!"); }
}