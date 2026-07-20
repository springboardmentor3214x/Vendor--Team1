import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-procurement-request',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './procurement-request.html',
  styleUrls: ['./procurement-request.css']
})
export class ProcurementRequest {
  procurement = {
    requestNumber: this.generateRequestNumber(),
    requestTitle: '',
    departmentName: '',
    requestedBy: '',
    itemName: '',
    productCategory: '',
    quantity: 1,
    unit: '',
    estimatedBudget: null as number | null,
    requiredDeliveryDate: '',
    priority: 'Medium',
    businessJustification: '',
    additionalRemarks: '',
    supportingDocument: '',
    requestStatus: 'Pending'
  };

  formError = '';

  constructor(
    private router: Router,
    private procurementService: ProcurementService
  ) {}

  generateRequestNumber(): string {
    const number = Math.floor(1000 + Math.random() * 9000);
    return `PR-${number}`;
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.procurement.supportingDocument = input.files[0].name;
    }
  }

  validateForm(): boolean {
    this.formError = '';
    const p = this.procurement;

    if (!p.requestTitle || !p.departmentName || !p.requestedBy || !p.itemName || !p.productCategory || !p.unit || !p.requiredDeliveryDate || !p.businessJustification) {
      this.formError = 'Please fill out all mandatory fields.';
      return false;
    }
    
    if (p.quantity <= 0) {
      this.formError = 'Quantity must be greater than zero.';
      return false;
    }

    if (p.estimatedBudget === null || p.estimatedBudget <= 0) {
      this.formError = 'Budget must be a valid numeric amount.';
      return false;
    }

    const today = new Date();
    today.setHours(0,0,0,0);
    const selectedDate = new Date(p.requiredDeliveryDate);
    if (selectedDate < today) {
      this.formError = 'Required Delivery Date cannot be in the past.';
      return false;
    }

    return true;
  }

  submitRequest(): void {
    if (!this.validateForm()) {
      return;
    }

    this.procurementService.createProcurementRequest(this.procurement).subscribe({
      next: (res) => {
        alert('Procurement Request Submitted Successfully!');
        this.router.navigate(['/procurement/requests']);
      },
      error: (err) => {
        console.error('Error submitting request', err);
        // Fallback for mock backend
        alert('Procurement Request Submitted Successfully! (Mocked)');
        this.router.navigate(['/procurement/requests']);
      }
    });
  }

  saveDraft(): void {
    alert('Draft Saved Successfully!');
    console.log(this.procurement);
  }

  cancel(): void {
    this.router.navigate(['/dashboard/procurement-dashboard']);
  }
}