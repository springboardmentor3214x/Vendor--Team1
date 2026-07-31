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
              date: p.created_at ? p.created_at.slice(0, 10) : new Date().toISOString().slice(0, 10),
              deadline: deadline,
              status: p.status || 'Pending'
            };
          });
        } else {
          this.orders = [];
        }
        this.cdr.markForCheck();
      },
      error: (err: any) => {
        this.loading = false;
        console.error('Failed to load orders', err);
        this.errorMsg = 'Failed to load purchase orders from backend.';
        this.cdr.markForCheck();
      }
    });
  }
}

const PLACEHOLDER_VENDOR_ORDERS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorOrders(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_ORDERS_ROWS;
  }
  return rows.filter((row) => !!row);
}
