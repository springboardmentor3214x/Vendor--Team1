import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { CommunicationService } from '../../core/services/communication.service';
import { ReliabilityService } from '../../core/services/reliability.service';

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
export class SupplyChainDashboard implements OnInit {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities: any[] = [];
  isLoading = true;

  avgReliabilityScore = 0;
  onTimeDelivery = 0;
  defectRate = 0;
  atRiskVendors = 0;

  constructor(
    private commService: CommunicationService,
    private reliabilityService: ReliabilityService
  ) {}

  ngOnInit(): void {
    this.refresh();
    this.loadMetrics();
  }

  loadMetrics() {
    this.reliabilityService.getDashboard().subscribe({
      next: (res) => {
        if (res) {
          this.avgReliabilityScore = Math.round(res.average_reliability_score || 0);
          this.atRiskVendors = res.high_risk_count || 0;
          this.onTimeDelivery = Math.round(res.average_reliability_score || 0);
          this.defectRate = res.average_reliability_score ? Math.max(0, Math.round(100 - res.average_reliability_score)) : 0;
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
    if (status.includes('Completed') || status.includes('Delivered')) return 'success';
    if (status.includes('Warning') || status.includes('Progress')) return 'warning';
    return 'default';
  }
}