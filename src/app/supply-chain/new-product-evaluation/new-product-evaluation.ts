import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

// UI Components
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-new-product-evaluation',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './new-product-evaluation.html',
  styleUrls: ['./new-product-evaluation.css']
})
export class NewProductEvaluation {
  evaluation = {
    poNumber: '',
    vendorName: '',
    inspectionDate: '',
    materialQuality: 5,
    packagingQuality: 5,
    quantityAccuracy: 5,
    specCompliance: 5,
    productDefects: 'None',
    remarks: ''
  };

  formError: string = '';

  constructor(private router: Router) {}

  submitEvaluation() {
    if (!this.evaluation.poNumber || !this.evaluation.vendorName || !this.evaluation.inspectionDate) {
      this.formError = 'Please fill in all required fields marked with an asterisk (*).';
      return;
    }

    this.formError = '';
    // Submit logic here
    console.log('Submitting product evaluation:', this.evaluation);
    this.router.navigate(['/supply-chain/product-quality']);
  }

  cancel() {
    this.router.navigate(['/supply-chain/product-quality']);
  }
}
