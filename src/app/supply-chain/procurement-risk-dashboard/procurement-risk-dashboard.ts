import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-procurement-risk-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './procurement-risk-dashboard.html',
  styleUrls: ['./procurement-risk-dashboard.css']
})
export class ProcurementRiskDashboard {
  highRiskVendors = [
    { id: 3, name: 'Apex Suppliers Ltd.', category: 'Raw Materials', riskScore: 85, issue: 'Financial instability detected in Q3 report; 4 consecutive delivery delays.', actionRequired: 'Hold all pending POs' },
    { id: 8, name: 'TechBuild Inc.', category: 'IT Equipment', riskScore: 78, issue: 'Failed quality inspection on last 2 batches.', actionRequired: 'Require secondary QA check' }
  ];

  mediumRiskVendors = [
    { id: 2, name: 'Global Logistics Inc.', category: 'Services', riskScore: 45, issue: 'Minor communication delays.', actionRequired: 'Monitor closely' },
    { id: 5, name: 'Industrial Metals', category: 'Raw Materials', riskScore: 55, issue: 'Price volatility on recent contracts.', actionRequired: 'Review next contract renewal' }
  ];

  getBadgeClass(risk: string): any {
    switch (risk) {
      case 'High': return { 'background': 'rgba(255, 59, 48, 0.1)', 'color': '#ff3b30' };
      case 'Medium': return { 'background': 'rgba(255, 204, 0, 0.1)', 'color': '#d4a000' };
      default: return {};
    }
  }
}
