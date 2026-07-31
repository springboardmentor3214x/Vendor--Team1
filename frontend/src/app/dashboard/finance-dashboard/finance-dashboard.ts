import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';

import { InvoiceService } from '../../core/services/invoice.service';
import { CommunicationService } from '../../core/services/communication.service';

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
export class FinanceDashboard implements OnInit {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];

  recentActivities: any[] = [];
  isLoading = true;

  pendingPaymentsCount = 0;
  invoicesProcessedCount = 0;
  overdueCount = 0;
  totalSpend = '₹0';

  constructor(
    private invoiceService: InvoiceService,
    private commService: CommunicationService
  ) {}

  ngOnInit(): void {
    this.refresh();
  }

  refresh() {
    this.isLoading = true;
    this.invoiceService.getInvoices().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.length > 0) {
          this.invoicesProcessedCount = res.length;
          this.pendingPaymentsCount = res.filter(i => i.payment_status !== 'Paid').length;
          this.overdueCount = res.filter(i => i.payment_status === 'Overdue').length;

          const sum = res.filter(i => i.payment_status === 'Paid').reduce((acc, i) => acc + (i.total_amount || 0), 0);
          this.totalSpend = `₹${sum.toLocaleString('en-IN')}`;

          this.recentActivities = res.slice(0, 5).map(i => ({
            date: i.issue_date ? new Date(i.issue_date).toLocaleDateString() : new Date().toLocaleDateString(),
            activity: `Invoice #${i.invoice_number || i.id} for $${(i.total_amount || 0).toLocaleString()} (${i.vendor_name || 'Vendor'})`,
            status: i.payment_status || 'Pending'
          }));
        } else {
          this.invoicesProcessedCount = 0;
          this.pendingPaymentsCount = 0;
          this.overdueCount = 0;
          this.totalSpend = '₹0';
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
    if (status.includes('Completed') || status.includes('Paid')) return 'success';
    if (status.includes('Pending') || status.includes('Review')) return 'warning';
    return 'default';
  }
}