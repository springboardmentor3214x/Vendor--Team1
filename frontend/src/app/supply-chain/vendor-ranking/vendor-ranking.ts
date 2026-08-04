import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { ReliabilityService } from '../../core/services/reliability.service';
import { ReportsService } from '../../core/services/reports.service';

interface RankingRecord {
  rank: number;
  vendorName: string;
  category: string;
  overallScore: number;
  deliveryScore: number;
  qualityScore: number;
  commScore: number;
  serviceRating: number;
  riskLevel: string;
  trend: 'Up' | 'Down' | 'Stable';
}

@Component({
  selector: 'app-vendor-ranking',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button, Table],
  templateUrl: './vendor-ranking.html',
  styleUrls: ['./vendor-ranking.css']
})
export class VendorRanking implements OnInit {
  rankings: RankingRecord[] = [];
  isLoading = true;
  errorMsg = '';

  categories = ['All', 'IT Vendors', 'Service Providers', 'Raw Material Suppliers',
                'Logistics Partners', 'Equipment Vendors', 'Maintenance Vendors'];
  selectedCategory = 'All';

  constructor(
    private reliabilityService: ReliabilityService,
    private reportsService: ReportsService
  ) {}

  ngOnInit() {
    this.loadRankings();
  }

  onCategoryChange(): void {
    this.loadRankings();
  }

  exportRanking(): void {
    this.errorMsg = '';
    this.reportsService.downloadExcel('vendor-performance', {
      category: this.selectedCategory
    }).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vendor_ranking.xlsx';
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: () => this.errorMsg = 'Could not export the ranking.'
    });
  }

  loadRankings() {
    this.isLoading = true;
    this.errorMsg = '';
    this.reliabilityService.getRankings(
      this.selectedCategory !== 'All' ? this.selectedCategory : undefined
    ).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res) {
          this.rankings = res.map((r: any, idx: number) => ({
            rank: r.vendor_rank || (idx + 1),
            vendorName: r.company_name || r.vendor_name,
            category: r.category || 'General',
            overallScore: r.reliability_score || 0,
            deliveryScore: r.delivery_score || 0,
            qualityScore: r.quality_score || 0,
            commScore: r.communication_score || 0,
            serviceRating: r.service_score ? (r.service_score / 20) : 0,
            riskLevel: r.procurement_risk_level ? r.procurement_risk_level.replace(' Risk', '') : 'Medium',
            trend: (r.reliability_score >= 80 ? 'Up' : (r.reliability_score >= 60 ? 'Stable' : 'Down')) as any
          }));
        }
      },
      error: () => {
        this.isLoading = false;
        this.errorMsg = 'Could not load vendor rankings.';
      }
    });
  }

  getBadgeClass(risk: string): any {
    switch (risk) {
      case 'Low': return { 'background': 'rgba(52, 199, 89, 0.1)', 'color': '#34c759' };
      case 'High': return { 'background': 'rgba(255, 59, 48, 0.1)', 'color': '#ff3b30' };
      case 'Medium': return { 'background': 'rgba(255, 204, 0, 0.1)', 'color': '#d4a000' };
      default: return {};
    }
  }
}
