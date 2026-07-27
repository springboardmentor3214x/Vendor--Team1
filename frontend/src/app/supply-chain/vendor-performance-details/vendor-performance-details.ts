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
}

const PLACEHOLDER_VENDOR_PERFORMANCE_DETAILS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorPerformanceDetails(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_PERFORMANCE_DETAILS_ROWS;
}
