import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';
import { CommunicationService } from '../../core/services/communication.service';

@Component({
  selector: 'app-audit-logs',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, InputComponent, Table],
  templateUrl: './audit-logs.html',
  styleUrls: ['./audit-logs.css']
})
export class AuditLogs implements OnInit {
  loading = true;
  errorMsg = '';

  allLogs: any[] = [];
  logs: any[] = [];

  searchText = '';
  selectedModule = 'All';
  modules = ['All', 'Vendor', 'Procurement', 'Contract', 'Invoice', 'Compliance', 'Communication', 'Delivery', 'User'];

  constructor(private communicationService: CommunicationService) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  loadLogs(): void {
    this.loading = true;
    this.errorMsg = '';
    this.communicationService.getActivityLogs(
      this.selectedModule === 'All' ? undefined : this.selectedModule,
      200
    ).subscribe({
      next: (res) => {
        this.loading = false;
        this.allLogs = (res || []).map(l => ({
          timestamp: l.timestamp ? new Date(l.timestamp).toLocaleString() : '-',
          user: l.user_name || 'System',
          module: l.module_name || '-',
          action: l.action,
          entity: l.related_record || '-',
          details: l.details || '',
          ip: l.ip_address || '-'
        }));
        this.applySearch();
      },
      error: () => {
        this.loading = false;
        this.allLogs = [];
        this.logs = [];
        this.errorMsg = 'Could not load activity logs. Please try again.';
      }
    });
  }

  applySearch(): void {
    const term = this.searchText.toLowerCase().trim();
    this.logs = !term
      ? [...this.allLogs]
      : this.allLogs.filter(l =>
          l.user.toLowerCase().includes(term) ||
          l.action.toLowerCase().includes(term) ||
          l.module.toLowerCase().includes(term) ||
          l.entity.toLowerCase().includes(term) ||
          l.details.toLowerCase().includes(term) ||
          l.ip.toLowerCase().includes(term)
        );
  }

  onModuleChange(): void {
    this.loadLogs();
  }
}
