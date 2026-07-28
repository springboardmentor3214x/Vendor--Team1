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

  constructor(
    private contractService: ContractService,
    private commService: CommunicationService
  ) {}

  ngOnInit(): void {
    this.refresh();
  }

  refresh() {
    this.isLoading = true;
    this.contractService.getComplianceDashboard().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res) {
          this.complianceRate = Math.round(res.compliance_rate || 100);
          this.pendingAudits = res.pending_reviews || 0;
          this.flaggedIssues = res.non_compliant_count || 0;
          this.reportsGenerated = res.total_records || 0;
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });

    this.commService.getActivityLogs('All', 10).subscribe({
      next: (logs) => {
        if (logs && logs.length > 0) {
          this.recentActivities = logs.map(l => ({
            date: new Date(l.timestamp).toLocaleDateString(),
            activity: `${l.user_name || 'Auditor'}: ${l.action} (${l.details || l.module_name})`,
            status: 'Passed'
          }));
        } else {
          this.recentActivities = [];
        }
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'default' {
    if (status.includes('Passed') || status.includes('Completed')) return 'success';
    if (status.includes('Pending') || status.includes('Progress')) return 'warning';
    if (status.includes('Flagged')) return 'primary';
    return 'default';
  }
}