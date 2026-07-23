import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

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
export class Dashboard implements OnInit {

  columns: TableColumn[] = [
    { key: 'companyName', label: 'Vendor Name' },
    { key: 'category', label: 'Category' },
    { key: 'reliabilityScore', label: 'Reliability' },
    { key: 'status', label: 'Status' }
  ];

  recentVendors: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<any[]>('/vendors/recent?limit=5').subscribe({
      next: (vendors) => {
        this.recentVendors = vendors.map(v => ({
          companyName: v.company_name,
          category: v.category,
          reliabilityScore: v.reliability_score
            ? v.reliability_score.toFixed(1) + ' ⭐'
            : 'N/A',
          status: v.status
        }));
      },
      error: () => {
        // Silently fail — table shows empty state
      }
    });
  }

  refresh() {
    this.ngOnInit();
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'danger' | 'default' {
    switch (status) {
      case 'Approved': return 'success';
      case 'Pending':  return 'warning';
      case 'High Risk': return 'danger';
      default: return 'default';
    }
  }
}