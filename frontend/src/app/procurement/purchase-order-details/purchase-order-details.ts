import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { PurchaseOrderService } from '../../core/services/purchase-order.service';

export interface PurchaseOrderDetailsMock {
  id: number;
  poNumber: string;
  prNumber: string;
  vendorName: string;
  vendorAddress: string;
  contactPerson: string;
  productDetails: string;
  quantity: number;
  unitPrice: number;
  totalCost: number;
  taxDetails: string;
  shippingAddress: string;
  expectedDeliveryDate: string;
  paymentTerms: string;
  status: string;
  createdDate: string;
  approvedBy: string;
}

@Component({
  selector: 'app-purchase-order-details',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './purchase-order-details.html',
  styleUrls: ['./purchase-order-details.css'],
})
export class PurchaseOrderDetails implements OnInit {
  poId: string | null = null;
  po: PurchaseOrderDetailsMock | null = null;

  constructor(
    private route: ActivatedRoute, 
    private router: Router,
    private poService: PurchaseOrderService
  ) {}

  ngOnInit(): void {
    this.poId = this.route.snapshot.paramMap.get('id');
    if (this.poId) {
      this.loadPO(this.poId);
    }
  }

  loadPO(id: string): void {
    this.poService.getPurchaseOrderById(id).subscribe({
      next: (res) => {
        this.po = res;
      },
      error: (err) => {
        console.error('Error fetching PO details', err);
        // Mock Data fallback
        this.po = {
          id: Number(id) || 1,
          poNumber: `PO-84${id || 92}`,
          prNumber: 'PR-1024',
          vendorName: 'TechCorp Ltd',
          vendorAddress: '456 Vendor Lane, Supplier City',
          contactPerson: 'Jane Doe',
          productDetails: 'Office Supplies Q3',
          quantity: 50,
          unitPrice: 1000,
          totalCost: 50000,
          taxDetails: '18% GST',
          shippingAddress: 'HQ Warehouse, 123 Main St, Tech City',
          expectedDeliveryDate: '15 Aug 2026',
          paymentTerms: 'Net 30',
          status: 'Ordered',
          createdDate: '16 Jul 2026',
          approvedBy: 'Admin User'
        };
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' {
    if (status === 'Completed' || status === 'Delivered') return 'success';
    if (status === 'Ordered') return 'primary';
    if (status === 'Pending') return 'warning';
    if (status === 'Cancelled') return 'danger';
    return 'default';
  }

  printPO(): void {
    window.print();
  }

  downloadPDF(): void {
    alert('Downloading PDF...');
  }
}
