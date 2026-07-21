import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

// UI Components
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-submit-service-rating',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './submit-service-rating.html',
  styleUrls: ['./submit-service-rating.css']
})
export class SubmitServiceRating {
  rating = {
    poNumber: '',
    vendorName: '',
    professionalism: 5,
    customerSupport: 5,
    documentationQuality: 5,
    flexibility: 5,
    communication: 5,
    issueResolution: 5,
    comments: ''
  };

  formError: string = '';

  constructor(private router: Router) {}

  submitRating() {
    if (!this.rating.poNumber || !this.rating.vendorName) {
      this.formError = 'Please fill in all required fields marked with an asterisk (*).';
      return;
    }

    this.formError = '';
    // Submit logic here
    console.log('Submitting service rating:', this.rating);
    this.router.navigate(['/supply-chain/service-rating']);
  }

  cancel() {
    this.router.navigate(['/supply-chain/service-rating']);
  }
}
