import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

import { DashboardCards } from './dashboard-cards/dashboard-cards';
import { Table, TableColumn } from '../ui/table/table';
import { Badge } from '../ui/badge/badge';
import { Button } from '../ui/button/button';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    DashboardCards,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard {
  columns: TableColumn[] = [
    { key: 'name', label: 'Vendor Name' },
    { key: 'category', label: 'Category' },
    { key: 'rating', label: 'Rating' },
    { key: 'status', label: 'Status' }
  ];

  recentVendors = [
    { name: 'ABC Pvt Ltd', category: 'Electronics', rating: '4.8 ⭐', status: 'Approved' },
    { name: 'Delta Steel', category: 'Manufacturing', rating: '4.2 ⭐', status: 'Pending' },
    { name: 'Tech Solutions', category: 'Software', rating: '4.9 ⭐', status: 'Approved' },
    { name: 'Global Logistics', category: 'Transport', rating: '3.7 ⭐', status: 'High Risk' }
  ];

  getBadgeVariant(status: string): 'success' | 'warning' | 'danger' | 'default' {
    switch(status) {
      case 'Approved': return 'success';
      case 'Pending': return 'warning';
      case 'High Risk': return 'danger';
      default: return 'default';
    }
  }
}