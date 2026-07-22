import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

interface RankingRecord {
  rank: number;
  vendorName: string;
  category: string;
  overallScore: number;
  deliveryScore: number;
  qualityScore: number;
  commScore: number;
  serviceRating: number;
  trend: 'Up' | 'Down' | 'Stable';
}

@Component({
  selector: 'app-vendor-ranking',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './vendor-ranking.html',
  styleUrls: ['./vendor-ranking.css']
})
export class VendorRanking implements OnInit {
  rankings: RankingRecord[] = [];

  ngOnInit() {
    const rawData = [
      { vendorName: 'TechCorp Solutions', category: 'IT Equipment', overallScore: 94.5, deliveryScore: 95, qualityScore: 98, commScore: 90, serviceRating: 4.8, trend: 'Up' },
      { vendorName: 'Global Logistics Inc.', category: 'Services', overallScore: 88.2, deliveryScore: 85, qualityScore: 92, commScore: 88, serviceRating: 4.5, trend: 'Stable' },
      { vendorName: 'Prime Raw Materials', category: 'Raw Materials', overallScore: 78.4, deliveryScore: 70, qualityScore: 85, commScore: 75, serviceRating: 3.5, trend: 'Down' },
      { vendorName: 'Office Depot', category: 'Office Supplies', overallScore: 85.0, deliveryScore: 88, qualityScore: 84, commScore: 82, serviceRating: 4.0, trend: 'Stable' },
      { vendorName: 'Industrial Metals', category: 'Raw Materials', overallScore: 91.0, deliveryScore: 90, qualityScore: 94, commScore: 89, serviceRating: 4.6, trend: 'Up' }
    ];

    // Sort descending by overallScore
    rawData.sort((a, b) => b.overallScore - a.overallScore);

    // Assign rank
    this.rankings = rawData.map((data, index) => ({
      ...data,
      rank: index + 1,
      trend: data.trend as 'Up' | 'Down' | 'Stable'
    }));
  }
}
