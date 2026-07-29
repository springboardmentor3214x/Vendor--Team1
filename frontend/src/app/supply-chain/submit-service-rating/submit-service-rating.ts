import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

import { PerformanceService } from '../../core/services/performance.service';
import { ProcurementService } from '../../core/services/procurement.service';

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
export class SubmitServiceRating implements OnInit {

  rating = {
    procurementId: null as number | null,
    professionalism: 5,
    customerSupport: 5,
    documentationQuality: 5,
    flexibility: 5,
    communication: 5,
    issueResolution: 5,
    comments: ''
  };

  procurements: any[] = [];
  loadingProcurements = true;
  formError = '';
  submitting = false;

  constructor(
    private router: Router,
    private performanceService: PerformanceService,
    private procurementService: ProcurementService
  ) {}

  ngOnInit(): void {
    this.procurementService.getAllProcurementRequests().subscribe({
      next: (res) => {
        this.loadingProcurements = false;

        this.procurements = (res || [])
          .filter(p => ['Delivered', 'Completed'].includes(p.status) && p.vendor_id)
          .map(p => ({
            id: p.id,
            vendorId: p.vendor_id,
            label: `${p.request_number} — ${p.item_name}`
          }));
      },
      error: () => {
        this.loadingProcurements = false;
        this.procurements = [];
        this.formError = 'Could not load completed procurements.';
      }
    });
  }

  get selectedProcurement(): any {
    return this.procurements.find(p => p.id === Number(this.rating.procurementId));
  }

  submitRating(): void {
    this.formError = '';

    const selected = this.selectedProcurement;
    if (!selected) {
      this.formError = 'Select the procurement request being rated.';
      return;
    }

    const scores = [
      this.rating.professionalism,
      this.rating.customerSupport,
      this.rating.documentationQuality,
      this.rating.flexibility,
      this.rating.communication,
      this.rating.issueResolution
    ];
    if (scores.some(s => s < 1 || s > 5)) {
      this.formError = 'All ratings must be between 1 and 5.';
      return;
    }

    this.submitting = true;
    this.performanceService.submitServiceRating({
      procurement_id: selected.id,
      vendor_id: selected.vendorId,
      professionalism: Number(this.rating.professionalism),
      customer_support: Number(this.rating.customerSupport),
      documentation_quality: Number(this.rating.documentationQuality),
      flexibility: Number(this.rating.flexibility),
      communication_effectiveness: Number(this.rating.communication),
      issue_resolution: Number(this.rating.issueResolution),
      comments: this.rating.comments || null
    }).subscribe({
      next: () => {
        this.submitting = false;
        this.router.navigate(['/supply-chain/service-rating']);
      },
      error: (err) => {
        this.submitting = false;
        this.formError = err.error?.detail || 'Could not save the rating. Please try again.';
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/supply-chain/service-rating']);
  }
}
