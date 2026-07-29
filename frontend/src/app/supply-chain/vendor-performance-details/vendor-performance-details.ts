import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface HistoryRow {
  poNumber: string;
  requestNumber: string;
  itemName: string;
  date: string | null;
  deliveryStatus: string;
  delayDays: number | null;
  qualityRating: number | null;
  serviceRating: number | null;
}

@Component({
  selector: 'app-vendor-performance-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './vendor-performance-details.html',
  styleUrls: ['./vendor-performance-details.css']
})
export class VendorPerformanceDetails implements OnInit {
  vendorId: string = '';
  isLoading = true;
  errorMsg = '';
  vendor: any = {
    id: '',
    name: 'Loading…',
    category: '',
    rating: 0,
    score: '0.0'
  };
  metrics: any = {};
  history: HistoryRow[] = [];
  constructor(
    private route: ActivatedRoute,
    private performanceService: PerformanceService
  ) {}
  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id') || '';
    if (!this.vendorId) {
      this.isLoading = false;
      this.errorMsg = 'No vendor was specified.';
      return;
    }
    this.loadVendorPerformance(this.vendorId);
  }
}

const PLACEHOLDER_VENDOR_PERFORMANCE_DETAILS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorPerformanceDetails(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_PERFORMANCE_DETAILS_ROWS;
  }
  return rows.filter((row) => !!row);
}
