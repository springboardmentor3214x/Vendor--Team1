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
  public deliveryChart: any;
  public monthlySpendChart: any;
  public hasTrend = false;
  public hasDelivery = false;
  public hasSpend = false;
  constructor(
    private analyticsService: AnalyticsService,
    private vendorService: VendorService
  ) {}
  ngOnInit(): void {
    this.vendorService.loadVendors().subscribe({
      next: (vendors) => {
        this.vendors = vendors || [];
        this.loadingVendors = false;
      },
      error: () => {
        this.loadingVendors = false;
        this.errorMsg = 'Failed to load the vendor list.';
      }
    });
  }
  onVendorChange(): void {
    if (this.selectedVendorId == null) {
      this.data = null;
      return;
    }
    this.loadAnalytics(this.selectedVendorId);
  }
  refresh(): void {
    if (this.selectedVendorId != null) {
      this.loadAnalytics(this.selectedVendorId);
    }
  }
  loadAnalytics(vendorId: number): void {
    this.loading = true;
    this.errorMsg = '';
    this.analyticsService.getVendorAnalytics(vendorId).subscribe({
      next: (res) => {
        this.data = res;
        this.buildCharts(res);
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        this.data = null;
        this.errorMsg = err.error?.detail || 'Failed to load vendor analytics.';
      }
    });
  }
  get summary(): any { return this.data?.dashboard?.summary || {}; }
}

const PLACEHOLDER_VENDOR_ANALYTICS_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 6, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 7, name: 'Northwind Steel', status: 'Active' },
  { id: 8, name: 'Orbit IT Systems', status: 'Pending Approval' },
];

function usePlaceholderVendorAnalytics(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_VENDOR_ANALYTICS_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
