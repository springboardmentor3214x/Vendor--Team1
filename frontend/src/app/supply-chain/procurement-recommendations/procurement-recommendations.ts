import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-procurement-recommendations',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './procurement-recommendations.html',
  styleUrls: ['./procurement-recommendations.css']
})
export class ProcurementRecommendations implements OnInit {
  categories = ['All', 'IT Vendors', 'Raw Material Suppliers', 'Logistics Partners', 'Service Providers'];
  selectedCategory = 'All';

  recommendations: any[] = [];
  isLoading = true;

  constructor(private reliabilityService: ReliabilityService) {}

  ngOnInit(): void {
    this.loadRecommendations();
  }

  onCategoryChange(cat: string): void {
    this.selectedCategory = cat;
    this.loadRecommendations();
  }

  loadRecommendations(): void {
    this.isLoading = true;
    this.reliabilityService.getRecommendations(this.selectedCategory !== 'All' ? this.selectedCategory : undefined).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res) {
          this.recommendations = res.map((r: any) => ({
            rank: r.vendor_rank || 1,
            vendorId: r.vendor_id,
            reason: r.recommendation_reason || '',
            suitableForHighPriority: r.suitable_for_high_priority !== false,
            name: r.company_name || r.vendor_name,
            score: r.reliability_score || 0,
            risk: r.procurement_risk_level ? r.procurement_risk_level.replace(' Risk', '') : 'Medium',
            match: Math.round(r.reliability_score || 0),
            status: r.recommendation_status || 'Recommended'
          }));
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }

  getMatchClass(match: number): any {
    if (match >= 80) return { 'color': '#34c759', 'font-weight': 'bold' };
    if (match >= 60) return { 'color': '#ff9500' };
    return { 'color': '#ff3b30' };
  }
}
