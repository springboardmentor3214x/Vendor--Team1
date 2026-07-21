import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-reliability-score-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button],
  templateUrl: './reliability-score-details.html',
  styleUrls: ['./reliability-score-details.css']
})
export class ReliabilityScoreDetails {
  vendorId: string | null = '';
  vendorName: string = 'TechCorp Solutions';
  overallScore: number = 94.5;
  riskLevel: string = 'Low';

  metrics = [
    { label: 'Delivery History', score: 95, icon: 'local_shipping', color: '#34c759' },
    { label: 'Product Quality', score: 98, icon: 'verified', color: '#34c759' },
    { label: 'Communication Efficiency', score: 90, icon: 'forum', color: '#34c759' },
    { label: 'Contract Compliance', score: 96, icon: 'gavel', color: '#34c759' },
    { label: 'Purchase History (Volume)', score: 85, icon: 'history', color: '#ffcc00' },
    { label: 'Issue Resolution', score: 92, icon: 'build', color: '#34c759' }
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id');
    // In a real app, fetch vendor details using this.vendorId
  }
}
