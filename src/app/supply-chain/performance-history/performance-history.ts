import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

interface HistoryRecord {
  cycleId: string;
  poNumber: string;
  vendorName: string;
  deliveryStatus: string;
  qualityRating: number;
  commRating: string;
  serviceRating: number;
  issuesRaised: number;
  issuesResolved: number;
  trend: 'Up' | 'Down' | 'Stable';
}

@Component({
  selector: 'app-performance-history',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './performance-history.html',
  styleUrls: ['./performance-history.css']
})
export class PerformanceHistory implements OnInit {
  history: HistoryRecord[] = [];

  ngOnInit() {
    this.history = [
      {
        cycleId: 'CYC-1001',
        poNumber: 'PO-2023-101',
        vendorName: 'TechCorp Solutions',
        deliveryStatus: 'Early',
        qualityRating: 5,
        commRating: 'Fast',
        serviceRating: 4.8,
        issuesRaised: 0,
        issuesResolved: 0,
        trend: 'Up'
      },
      {
        cycleId: 'CYC-1002',
        poNumber: 'PO-2023-095',
        vendorName: 'TechCorp Solutions',
        deliveryStatus: 'On-Time',
        qualityRating: 4,
        commRating: 'Acceptable',
        serviceRating: 4.0,
        issuesRaised: 1,
        issuesResolved: 1,
        trend: 'Stable'
      },
      {
        cycleId: 'CYC-1003',
        poNumber: 'PO-2023-103',
        vendorName: 'Prime Raw Materials',
        deliveryStatus: 'Delayed',
        qualityRating: 4,
        commRating: 'Slow',
        serviceRating: 3.5,
        issuesRaised: 2,
        issuesResolved: 2,
        trend: 'Down'
      }
    ];
  }

  getTrendIcon(trend: string): string {
    switch(trend) {
      case 'Up': return 'trending_up';
      case 'Down': return 'trending_down';
      case 'Stable': return 'trending_flat';
      default: return 'remove';
    }
  }

  getTrendColor(trend: string): string {
    switch(trend) {
      case 'Up': return '#34c759';
      case 'Down': return '#ff3b30';
      case 'Stable': return '#8e8e93';
      default: return '#000';
    }
  }
}
