import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-invoice-management',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './invoice-management.html',
  styleUrls: ['./invoice-management.css'],
})
export class InvoiceManagement implements OnInit {
  invoices: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';

  constructor(private procurementService: ProcurementService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadInvoices();
  }

  loadInvoices(): void {
    this.loading = true;
    this.errorMsg = '';
    this.procurementService.getAllProcurementRequests().subscribe({
      next: (data) => {
        this.loading = false;
        if (Array.isArray(data)) {
          this.invoices = data.map(p => {
            const amount = p.total_price || (p.unit_price && p.quantity ? p.unit_price * p.quantity : 0);
            return {
              id: p.id,
              invoiceNumber: 'INV-2026-' + (5000 + p.id),
              poNumber: 'PO-2026-' + (1000 + p.id),
              itemName: p.item_name,
              amount: amount,
              issueDate: p.created_at ? p.created_at.slice(0, 10) : '2026-07-30',
              dueDate: p.expected_delivery_date ? p.expected_delivery_date.slice(0, 10) : '2026-08-30',
              status: p.status === 'Completed' ? 'Paid' : p.status === 'Delivered' ? 'Pending Payment' : 'Pending'
            };
          });
        } else {
          this.invoices = [];
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load invoices', err);
        this.errorMsg = 'Failed to load invoices from server.';
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' | 'info' {
    switch (status) {
      case 'Paid': return 'success';
      case 'Pending Payment':
      case 'Pending': return 'warning';
      case 'Overdue':
      case 'Rejected': return 'danger';
      default: return 'default';
    }
  }

  processPayment(inv: any): void {
    if (confirm(`Process payment of $${inv.amount.toFixed(2)} for ${inv.invoiceNumber}?`)) {
      this.procurementService.completeRequest(inv.id.toString()).subscribe({
        next: () => this.loadInvoices(),
        error: (err) => alert('Failed to process payment: ' + (err.error?.detail || err.message))
      });
    }
  }
}
