import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-procurement-risk-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './procurement-risk-dashboard.html',
  styleUrls: ['./procurement-risk-dashboard.css']
})
export class ProcurementRiskDashboard implements OnInit {
  isLoading = true;
  errorMsg = '';

  totalVendors = 0;
  lowRiskVendors: any[] = [];
  mediumRiskVendors: any[] = [];
  highRiskVendors: any[] = [];

  constructor(private reliabilityService: ReliabilityService) {}

  ngOnInit(): void {
    this.loadRiskAssessment();
  }

  loadRiskAssessment(): void {
    this.isLoading = true;
    this.errorMsg = '';
    this.reliabilityService.getRiskAssessment().subscribe({
      next: (res) => {
        this.isLoading = false;
        this.totalVendors = res?.total_vendors ?? 0;
        this.highRiskVendors = this.map(res?.high_risk_vendors, 'High');
        this.mediumRiskVendors = this.map(res?.medium_risk_vendors, 'Medium');
        this.lowRiskVendors = this.map(res?.low_risk_vendors, 'Low');
      },
      error: () => {
        this.isLoading = false;
        this.highRiskVendors = [];
        this.mediumRiskVendors = [];
        this.lowRiskVendors = [];
        this.errorMsg = 'Could not load the risk assessment. Please try again.';
      }
    });
  }

  private map(list: any[] | undefined, band: 'Low' | 'Medium' | 'High'): any[] {
    return (list || []).map(v => ({
      id: v.vendor_id,
      name: v.company_name || v.vendor_name,
      category: v.category || 'General',
      riskScore: Math.round(v.reliability_score || 0),
      issue: v.warning_message || this.defaultIssue(band),
      actionRequired: this.defaultAction(band)
    }));
  }

  private defaultIssue(band: string): string {
    if (band === 'High') return 'Reliability below 50: repeated delivery delays, quality issues or slow communication.';
    if (band === 'Medium') return 'Reliability between 50 and 80: occasional delays or quality variance observed.';
    return 'Reliability at or above 80: consistent delivery, quality and responsiveness.';
  }

  private defaultAction(band: string): string {
    if (band === 'High') return 'Requires explicit confirmation before assignment';
    if (band === 'Medium') return 'Monitor closely';
    return 'Approved for standard procurement';
  }

  getBadgeClass(risk: string): any {
    switch (risk) {
      case 'High': return { 'background': 'rgba(255, 59, 48, 0.1)', 'color': '#ff3b30' };
      case 'Medium': return { 'background': 'rgba(255, 204, 0, 0.1)', 'color': '#d4a000' };
      case 'Low': return { 'background': 'rgba(52, 199, 89, 0.1)', 'color': '#248a3d' };
      default: return {};
    }
  }
}
