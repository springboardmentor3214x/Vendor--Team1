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
}

const PLACEHOLDER_VENDOR_RANKING_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorRanking(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_RANKING_ROWS;
}
