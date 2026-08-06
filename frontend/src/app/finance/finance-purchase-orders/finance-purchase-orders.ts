import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-finance-purchase-orders',
  standalone: true,
  imports: [CommonModule, Card, Button, Badge],
  templateUrl: './finance-purchase-orders.html',
  styleUrls: ['./finance-purchase-orders.css']
})
export class FinancePurchaseOrders implements OnInit {
  orders: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';

  constructor(private procurementService: ProcurementService) {}

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
            return {
              id: p.id,
              poNumber: 'PO-2026-' + (1000 + p.id),
              itemName: p.item_name,
              quantity: p.quantity,
              amount: amount,
              status: p.status || 'Pending'
            };
          });
        } else {
          this.orders = [];
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load purchase orders', err);
        this.errorMsg = 'Failed to load purchase orders from backend.';
      }
    });
  }

  completePO(order: any): void {
    this.procurementService.completeRequest(order.id).subscribe({
      next: () => this.loadOrders(),
      error: (err) => alert('Failed to complete PO: ' + (err.error?.detail || err.message))
    });
  }

  getBadgeVariant(status: string): 'primary' | 'danger' | 'success' | 'warning' | 'default' | 'info' {
    switch (status) {
      case 'Completed':
      case 'Delivered': return 'success';
      case 'Approved':
      case 'Order Placed':
      case 'Dispatched': return 'info';
      case 'Pending': return 'warning';
      default: return 'default';
    }
  }
}