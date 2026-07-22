import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { NgApexchartsModule } from 'ng-apexcharts';
import { AnalyticsService } from '../../core/services/analytics.service';
import { VendorService } from '../../services/vendor';

@Component({
  selector: 'app-vendor-analytics',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, NgApexchartsModule],
  templateUrl: './vendor-analytics.html',
  styleUrls: ['./vendor-analytics.css']
})
export class VendorAnalytics implements OnInit {
  vendors: any[] = [];
  selectedVendorId: number | null = null;
  loadingVendors = true;
  loading = false;
  errorMsg = '';
  data: any = null;
  public reliabilityTrendChart: any;
  public subScoreChart: any;
}

const PLACEHOLDER_VENDOR_ANALYTICS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorAnalytics(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_ANALYTICS_ROWS;
}
