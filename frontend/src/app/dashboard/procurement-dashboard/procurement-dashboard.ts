import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { CommunicationService } from '../../core/services/communication.service';
import { AnalyticsService } from '../../core/services/analytics.service';

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
export class ProcurementDashboard implements OnInit {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities: any[] = [];
  isLoading = true;

  openRequests = 0;
  activePOs = 0;
  awaitingApproval = 0;
  completedOrders = 0;

  constructor(
    private commService: CommunicationService,
    private analyticsService: AnalyticsService
  ) {}

  ngOnInit(): void {
    this.refresh();
    this.loadMetrics();
  }

  loadMetrics() {
    this.analyticsService.getProcurementManagerDashboard().subscribe({
      next: (data) => {
        if (data && data.summary) {
          this.openRequests = data.summary.total_procurement_requests || 0;
          this.activePOs = data.summary.active_purchase_orders || 0;
          this.awaitingApproval = data.summary.pending_approvals || 0;
          this.completedOrders = data.summary.completed_orders || 0;
        }
      }
    });
  }

  refresh() {
    this.isLoading = true;
    this.commService.getActivityLogs('All', 10).subscribe({
      next: (logs) => {
        this.isLoading = false;
        if (logs && logs.length > 0) {
          this.recentActivities = logs.map(l => ({
            date: new Date(l.timestamp).toLocaleDateString(),
            activity: `${l.user_name || 'System'}: ${l.action} (${l.details || l.module_name})`,
            status: 'Completed'
          }));
        } else {
          this.recentActivities = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.recentActivities = [];
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Completed')) return 'success';
    if (status.includes('Pending') || status.includes('Progress')) return 'warning';
    if (status.includes('Transit')) return 'primary';
    return 'default';
  }
}