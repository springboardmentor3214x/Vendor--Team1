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
export class NewProductEvaluation implements OnInit {

  evaluation = {
    procurementId: null as number | null,
    inspectionDate: new Date().toISOString().slice(0, 10),
    materialQuality: 5,
    packagingQuality: 5,
    quantityAccuracy: 5,
    specCompliance: 5,
    defectCount: 0,
    remarks: ''
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
        this.formError = 'Could not load delivered procurements.';
      }
    });
  }

  get selectedProcurement(): any {
    return this.procurements.find(p => p.id === Number(this.evaluation.procurementId));
  }

  submitEvaluation(): void {
    this.formError = '';

    const selected = this.selectedProcurement;
    if (!selected) {
      this.formError = 'Select the purchase order / procurement request being evaluated.';
      return;
    }
    if (!this.evaluation.inspectionDate) {
      this.formError = 'Inspection date is required.';
      return;
    }

    const ratings = [
      this.evaluation.materialQuality,
      this.evaluation.packagingQuality,
      this.evaluation.quantityAccuracy,
      this.evaluation.specCompliance
    ];
    if (ratings.some(r => r < 1 || r > 5)) {
      this.formError = 'All quality ratings must be between 1 and 5.';
      return;
    }
    if (this.evaluation.defectCount < 0) {
      this.formError = 'Defect count cannot be negative.';
      return;
    }

    this.submitting = true;
    this.performanceService.recordQuality({
      procurement_id: selected.id,
      vendor_id: selected.vendorId,
      material_quality: Number(this.evaluation.materialQuality),
      packaging_quality: Number(this.evaluation.packagingQuality),
      quantity_accuracy: Number(this.evaluation.quantityAccuracy),
      specification_compliance: Number(this.evaluation.specCompliance),
      defect_count: Number(this.evaluation.defectCount),
      remarks: this.evaluation.remarks || null
    }).subscribe({
      next: () => {
        this.submitting = false;
        this.router.navigate(['/supply-chain/product-quality']);
      },
      error: (err) => {
        this.submitting = false;
        this.formError = err.error?.detail || 'Could not save the evaluation. Please try again.';
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/supply-chain/product-quality']);
  }
}
