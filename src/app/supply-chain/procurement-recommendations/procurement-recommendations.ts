import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-procurement-recommendations',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './procurement-recommendations.html',
  styleUrls: ['./procurement-recommendations.css']
})
export class ProcurementRecommendations {
  categories = ['IT Equipment', 'Raw Materials', 'Office Supplies', 'Services'];
  selectedCategory = 'IT Equipment';

  recommendations = [
    { rank: 1, name: 'TechCorp Solutions', score: 94.5, risk: 'Low', match: 98, status: 'Highly Recommended' },
    { rank: 2, name: 'ElectroTech Partners', score: 91.0, risk: 'Low', match: 92, status: 'Recommended' },
    { rank: 3, name: 'NextGen Systems', score: 85.5, risk: 'Medium', match: 80, status: 'Alternative' },
    { rank: 4, name: 'TechBuild Inc.', score: 78.0, risk: 'High', match: 65, status: 'Avoid' }
  ];

  getMatchClass(match: number): any {
    if (match >= 90) return { 'color': '#34c759', 'font-weight': 'bold' };
    if (match >= 80) return { 'color': '#ff9500' };
    return { 'color': '#ff3b30' };
  }
}
