import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-vendor-reliability-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table, InputComponent],
  templateUrl: './vendor-reliability-dashboard.html',
  styleUrls: ['./vendor-reliability-dashboard.css']
})
export class VendorReliabilityDashboard {
  summary = {
    totalVendors: 145,
    averageScore: 82.5,
    highReliability: 45,
    mediumReliability: 70,
    highRisk: 30
  };

  vendors = [
    { id: 1, name: 'TechCorp Solutions', category: 'IT Equipment', score: 94.5, risk: 'Low', recommendation: 'Highly Recommended' },
    { id: 2, name: 'Global Logistics Inc.', category: 'Services', score: 88.2, risk: 'Medium', recommendation: 'Recommended' },
    { id: 3, name: 'Apex Suppliers Ltd.', category: 'Raw Materials', score: 45.0, risk: 'High', recommendation: 'Do Not Recommend' },
    { id: 4, name: 'Office Depot', category: 'Office Supplies', score: 91.0, risk: 'Low', recommendation: 'Recommended' },
    { id: 5, name: 'Industrial Metals', category: 'Raw Materials', score: 78.4, risk: 'Medium', recommendation: 'Review Required' }
  ];

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
