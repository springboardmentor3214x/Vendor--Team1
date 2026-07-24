import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-performance-trend-analysis',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button],
  templateUrl: './performance-trend-analysis.html',
  styleUrls: ['./performance-trend-analysis.css']
})
export class PerformanceTrendAnalysis implements OnInit {
  vendorId: string | null = '';
  vendorName: string = 'Loading…';
  isLoading = true;
  errorMsg = '';
  months: string[] = [];
  overallTrend = '';
  currentScore: number | null = null;
}

const PLACEHOLDER_PERFORMANCE_TREND_ANALYSIS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderPerformanceTrendAnalysis(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PERFORMANCE_TREND_ANALYSIS_ROWS;
}
