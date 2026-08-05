import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { InputComponent } from '../../ui/input/input';
import { ReliabilityService } from '../../core/services/reliability.service';
import { ReportsService } from '../../core/services/reports.service';

@Component({
  selector: 'app-vendor-reliability-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button, Table, InputComponent],
  templateUrl: './vendor-reliability-dashboard.html',
  styleUrls: ['./vendor-reliability-dashboard.css']
})
export class VendorReliabilityDashboard implements OnInit {
  isLoading = true;
  errorMsg = '';
  summary = {
    totalVendors: 0,
    averageScore: 0,
    highReliability: 0,
    mediumReliability: 0,
    highRisk: 0
  };

  allVendors: any[] = [];
  vendors: any[] = [];

  searchText = '';
  categoryFilter = '';
  riskFilter = '';
  categories = ['IT Vendors', 'Service Providers', 'Raw Material Suppliers',
                'Logistics Partners', 'Equipment Vendors', 'Maintenance Vendors'];

  constructor(
    private reliabilityService: ReliabilityService,
    private reportsService: ReportsService
  ) {}

  applyFilters(): void {
    const term = this.searchText.toLowerCase().trim();
    this.vendors = this.allVendors.filter(v => {
      const matchesSearch = !term || (v.name || '').toLowerCase().includes(term);
      const matchesCategory = !this.categoryFilter || v.category === this.categoryFilter;
      const matchesRisk = !this.riskFilter || v.risk === this.riskFilter;
      return matchesSearch && matchesCategory && matchesRisk;
    });
  }

  resetFilters(): void {
    this.searchText = '';
    this.categoryFilter = '';
    this.riskFilter = '';
    this.applyFilters();
  }

  exportReport(): void {
    this.errorMsg = '';
    this.reportsService.downloadExcel('vendor-performance', {
      category: this.categoryFilter || 'All'
    }).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vendor_reliability_report.xlsx';
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: () => this.errorMsg = 'Could not export the report.'
    });
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.isLoading = true;
    this.reliabilityService.getDashboard().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res) {
          this.summary = {
            totalVendors: res.total_vendors_evaluated || 0,
            averageScore: res.average_reliability_score || 0,
            highReliability: res.high_reliability_count || 0,
            mediumReliability: res.medium_reliability_count || 0,
            highRisk: res.high_risk_count || 0
          };
          this.allVendors = (res.top_ranked_vendors || []).map((v: any) => ({
            id: v.vendor_id,
            name: v.company_name || v.vendor_name,
            category: v.category || 'General',
            score: v.reliability_score || 0,
            risk: v.risk_level ? v.risk_level.replace(' Risk', '') : 'Medium',
            recommendation: v.reliability_score >= 80 ? 'Highly Recommended' : (v.reliability_score >= 50 ? 'Recommended' : 'Review Required')
          }));
          this.applyFilters();
        }
      },
      error: () => {
        this.isLoading = false;
        this.errorMsg = 'Could not load the reliability dashboard.';
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

  getRecommendationClass(rec: string): any {
    switch (rec) {
      case 'Highly Recommended': return { 'color': '#34c759', 'font-weight': 'bold' };
      case 'Recommended': return { 'color': '#34c759' };
      case 'Review Required': return { 'color': '#ffcc00' };
      case 'Do Not Recommend': return { 'color': '#ff3b30', 'font-weight': 'bold' };
      default: return {};
    }
  }
}
