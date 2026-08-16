import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface ServiceRecord {
  poNumber: string;
  vendorName: string;
  professionalism: number;
  customerSupport: number;
  documentationQuality: number;
  flexibility: number;
  communicationEffectiveness: number;
  issueResolution: number;
  overallRating: number;
  comments: string;
}

@Component({
  selector: 'app-service-rating',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './service-rating.html',
  styleUrls: ['./service-rating.css']
})
export class ServiceRating implements OnInit {
  ratings: ServiceRecord[] = [];
  isLoading = true;

  constructor(private performanceService: PerformanceService) {}

  ngOnInit() {
    this.loadRatings();
  }

  loadRatings() {
    this.isLoading = true;
    this.performanceService.getServiceRatings(1).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.length > 0) {
          this.ratings = res.map((r: any) => ({
            poNumber: `PO-${1000 + (r.procurement_id || r.id)}`,
            vendorName: `Vendor #${r.vendor_id}`,
            professionalism: r.professionalism || 5,
            customerSupport: r.customer_support || 5,
            documentationQuality: r.documentation_quality || 5,
            flexibility: r.flexibility || 5,
            communicationEffectiveness: r.communication_effectiveness || 5,
            issueResolution: r.issue_resolution || 5,
            overallRating: r.overall_rating || 5.0,
            comments: r.comments || 'Evaluated'
          }));
        } else {
          this.ratings = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.ratings = [];
      }
    });
  }
}
