import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-procurement-request',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule
  ],
  templateUrl: './procurement-request.html',
  styleUrl: './procurement-request.css'
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

    estimatedBudget: null,

    requiredDeliveryDate: '',

    priority: 'Medium',

    businessJustification: '',

    additionalRemarks: '',

    supportingDocument: '',

    requestStatus: 'Pending'

  };

  constructor(
    private router: Router
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

  submitRequest(): void {

    alert('Procurement Request Submitted Successfully!');

    console.log(this.procurement);

  }

  saveDraft(): void {

    alert('Draft Saved Successfully!');

    console.log(this.procurement);

  }

  cancel(): void {

    this.router.navigate(['/procurement-dashboard']);

  }

}