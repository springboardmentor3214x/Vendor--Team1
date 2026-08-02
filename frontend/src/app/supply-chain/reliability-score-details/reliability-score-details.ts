import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-reliability-score-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button],
  templateUrl: './reliability-score-details.html',
  styleUrls: ['./reliability-score-details.css']
})
export class ReliabilityScoreDetails implements OnInit {
  vendorId: string | null = '';
  vendorName: string = 'Loading...';
  overallScore: number = 0;
  riskLevel: string = 'Medium';
  isLoading = true;

  metrics: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private reliabilityService: ReliabilityService
  ) {}

  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id') || '1';
    this.loadDetails(this.vendorId);
  }

  loadDetails(id: string) {
    this.isLoading = true;
    this.reliabilityService.getDetails(id).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res) {
          this.vendorName = res.company_name || res.vendor_name;
          this.overallScore = res.reliability_score || 0;
          this.riskLevel = res.procurement_risk_level ? res.procurement_risk_level.replace(' Risk', '') : 'Medium';

          const f = res.reliability_factors || {};
          this.metrics = [
            { label: 'Delivery History', score: f.delivery_history?.score || 0, icon: 'local_shipping', color: '#34c759' },
            { label: 'Product Quality', score: f.product_quality?.score || 0, icon: 'verified', color: '#34c759' },
            { label: 'Communication Efficiency', score: f.communication_efficiency?.score || 0, icon: 'forum', color: '#34c759' },
            { label: 'Service Rating', score: f.service_ratings?.score || 0, icon: 'star', color: '#34c759' },
            { label: 'Purchase History (Volume)', score: f.purchase_history?.fulfillment_rate || 0, icon: 'history', color: '#ffcc00' }
          ];
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }
}
