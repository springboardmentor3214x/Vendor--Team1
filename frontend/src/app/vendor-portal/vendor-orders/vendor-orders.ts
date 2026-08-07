import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-vendor-orders',
  standalone: true,
  imports: [CommonModule, Card, Button, Badge],
  templateUrl: './vendor-orders.html',
  styleUrls: ['./vendor-orders.css']
})
export class VendorOrders implements OnInit {
  orders: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';

  constructor(
    private procurementService: ProcurementService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadOrders();
  }

  loadOrders(): void {
    this.loading = true;
    this.errorMsg = '';
    this.procurementService.getAllProcurementRequests().subscribe({
      next: (data) => {
        this.loading = false;
        if (Array.isArray(data)) {
          this.orders = data.map(p => {
            const amount = p.total_price || (p.unit_price && p.quantity ? p.unit_price * p.quantity : 0);
            const deadline = p.expected_delivery_date ? p.expected_delivery_date.slice(0, 10) : 'N/A';
            return {
              id: p.id,
              poNumber: 'PO-2026-' + (1000 + p.id),
              itemName: p.item_name,
              quantity: p.quantity,
              amount: amount,
              date: p.created_at ? p.created_at.slice(0, 10) : '2026-07-30',
              deadline: deadline,
              status: p.status || 'Pending'
            };
          });
        } else {
          this.orders = [];
        }
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load orders', err);
        this.errorMsg = 'Failed to load purchase orders from backend.';
        this.cdr.markForCheck();
      }
    });
  }

  dispatchOrder(order: any): void {
    this.procurementService.dispatchRequest(order.id).subscribe({
      next: () => this.loadOrders(),
      error: (err) => alert('Failed to dispatch: ' + (err.error?.detail || err.message))
    });
  }

  getBadgeVariant(status: string): 'primary' | 'danger' | 'success' | 'warning' | 'default' | 'info' {
    switch (status) {
      case 'Delivered':
      case 'Completed':
        return 'success';
      case 'Dispatched':
      case 'Order Placed':
      case 'Approved':
        return 'info';
      case 'Pending':
        return 'warning';
      default:
        return 'default';
    }
  }
}