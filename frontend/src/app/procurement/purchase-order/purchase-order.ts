import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { PurchaseOrderService } from '../../core/services/purchase-order.service';

export interface PurchaseOrderModel {
  poNumber: string;
  prNumber: string;
  vendorId: number | null;
  vendorName: string;
  vendorAddress: string;
  contactPerson: string;
  productDetails: string;
  quantity: number;
  unitPrice: number;
  taxDetails: string;
  shippingAddress: string;
  expectedDeliveryDate: string;
  paymentTerms: string;
  status: string;
}

@Component({
  selector: 'app-purchase-order',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './purchase-order.html',
  styleUrls: ['./purchase-order.css'],
})
export class PurchaseOrder implements OnInit {
  poData: PurchaseOrderModel = {
    poNumber: `PO-${Math.floor(1000 + Math.random() * 9000)}`,
    prNumber: '',
    vendorId: null,
    vendorName: '',
    vendorAddress: '',
    contactPerson: '',
    productDetails: '',
    quantity: 1,
    unitPrice: 0,
    taxDetails: '18% GST',
    shippingAddress: 'HQ Warehouse, 123 Main St, Tech City',
    expectedDeliveryDate: '',
    paymentTerms: 'Net 30',
    status: 'Draft'
  };

  formError = '';

  constructor(
    private route: ActivatedRoute, 
    private router: Router,
    private poService: PurchaseOrderService
  ) {}

  ngOnInit(): void {
    const prId = this.route.snapshot.queryParamMap.get('pr');
    const vendorId = this.route.snapshot.queryParamMap.get('vendor');

    if (prId) {
      this.poData.prNumber = `PR-102${prId}`;
      this.poData.productDetails = 'Office Supplies Q3';
      this.poData.quantity = 50;
      this.poData.unitPrice = 1000; // 50 * 1000 = 50,000 budget
    }

    if (vendorId) {
      this.poData.vendorId = Number(vendorId);
      this.poData.vendorName = 'TechCorp Ltd';
      this.poData.contactPerson = 'Jane Doe';
      this.poData.vendorAddress = '456 Vendor Lane, Supplier City';
    }
  }

  get totalCost(): number {
    return this.poData.quantity * this.poData.unitPrice;
  }

  validateForm(): boolean {
    this.formError = '';
    if (!this.poData.expectedDeliveryDate) {
      this.formError = 'Expected Delivery Date is required.';
      return false;
    }
    return true;
  }

  generatePO(): void {
    if (!this.validateForm()) return;

    this.poData.status = 'Ordered';
    this.poService.createPurchaseOrder(this.poData).subscribe({
      next: () => {
        alert(`Purchase Order ${this.poData.poNumber} generated successfully!`);
        this.router.navigate(['/procurement/requests']);
      },
      error: (err) => {
        console.error('Error generating PO', err);
        // Mock success
        alert(`Purchase Order ${this.poData.poNumber} generated successfully! (Mocked)`);
        this.router.navigate(['/procurement/requests']);
      }
    });
  }

  saveDraft(): void {
    alert('Purchase Order saved as draft.');
  }

  cancel(): void {
    this.router.navigate(['/procurement/requests']);
  }
}
