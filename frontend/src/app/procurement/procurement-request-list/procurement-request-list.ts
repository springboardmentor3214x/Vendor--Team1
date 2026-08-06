import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-procurement-request-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './procurement-request-list.html',
  styleUrls: ['./procurement-request-list.css'],
})
export class ProcurementRequestList implements OnInit {
  requests: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';

  constructor(private procurementService: ProcurementService) {}

  ngOnInit(): void {
    this.loadRequests();
  }

  loadRequests(): void {
    this.loading = true;
    this.errorMsg = '';
    this.procurementService.getAllProcurementRequests().subscribe({
      next: (res) => {
        this.loading = false;
        if (Array.isArray(res)) {
          this.requests = res.map(item => {
            const budget = item.total_price || (item.unit_price && item.quantity ? item.unit_price * item.quantity : 0);
            return {
              id: item.id,
              requestNumber: 'PR-2026-' + (1000 + item.id),
              title: item.item_name || 'Procurement Item',
              quantity: item.quantity || 1,
              budget: budget,
              status: item.status || 'Pending',
              vendorId: item.vendor_id,
              createdDate: item.created_at ? item.created_at.slice(0, 10) : '2026-07-30'
            };
          });
        } else {
          this.requests = [];
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Error fetching procurement requests', err);
        this.errorMsg = 'Failed to load procurement requests from server.';
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' | 'info' {
    switch (status) {
      case 'Approved':
      case 'Delivered':
      case 'Completed': return 'success';
      case 'Pending': return 'warning';
      case 'Rejected': return 'danger';
      case 'Order Placed':
      case 'Dispatched': return 'info';
      default: return 'default';
    }
  }

  deleteRequest(id: number): void {
    if (confirm('Are you sure you want to delete this procurement request?')) {
      this.procurementService.deleteProcurementRequest(id.toString()).subscribe({
        next: () => this.loadRequests(),
        error: (err) => alert('Failed to delete: ' + (err.error?.detail || err.message))
      });
    }
  }

  approveRequest(r: any): void {
    this.procurementService.approveRequest(r.id.toString(), {}).subscribe({
      next: () => this.loadRequests(),
      error: (err) => alert('Failed to approve: ' + (err.error?.detail || err.message))
    });
  }
}
