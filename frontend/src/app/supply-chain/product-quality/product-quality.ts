import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface QualityEvaluationRecord {
  poNumber: string;
  vendorName: string;
  inspectionDate: string;
  materialQuality: number;
  packagingQuality: number;
  quantityAccuracy: number;
  specCompliance: number;
  productDefects: string;
  overallRating: number;
  remarks: string;
}

@Component({
  selector: 'app-product-quality',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './product-quality.html',
  styleUrls: ['./product-quality.css']
})
export class ProductQuality implements OnInit {
  evaluations: QualityEvaluationRecord[] = [];
  isLoading = true;

  constructor(private performanceService: PerformanceService) {}

  ngOnInit() {
    this.loadQualityRecords();
  }

  loadQualityRecords() {
    this.isLoading = true;
    this.performanceService.getQualityRecords(1).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.length > 0) {
          this.evaluations = res.map((q: any) => ({
            poNumber: `PO-${1000 + (q.procurement_id || q.id)}`,
            vendorName: `Vendor #${q.vendor_id}`,
            inspectionDate: q.created_at ? new Date(q.created_at).toLocaleDateString() : 'N/A',
            materialQuality: q.material_quality || 5,
            packagingQuality: q.packaging_quality || 5,
            quantityAccuracy: q.quantity_accuracy || 5,
            specCompliance: q.specification_compliance || 5,
            productDefects: q.defect_count ? `${q.defect_count} defect(s)` : 'None',
            overallRating: q.overall_rating || 5,
            remarks: q.remarks || 'Inspected'
          }));
        } else {
          this.evaluations = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.evaluations = [];
      }
    });
  }
}
