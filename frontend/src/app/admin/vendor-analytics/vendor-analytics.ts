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
  get reliabilityScore(): number { return this.data?.reliability?.reliability_score ?? 0; }
  get riskLevel(): string { return this.data?.reliability?.procurement_risk_level || 'Not Rated'; }
  get recommendation(): string { return this.data?.reliability?.recommendation_status || '—'; }
  get overallTrend(): string { return this.data?.performance_trends?.overall_trend || 'Insufficient Data'; }

  riskClass(): string {
    switch (this.riskLevel) {
      case 'Low Risk': return 'risk-low';
      case 'Medium Risk': return 'risk-medium';
      case 'High Risk': return 'risk-high';
      default: return 'risk-none';
    }
  }

  formatCurrency(value: number): string {
    return `₹${(value || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  }

  buildCharts(res: any): void {

    const trends = res?.performance_trends?.monthly_trends || [];
    this.hasTrend = trends.length > 0;
    if (this.hasTrend) {
      const labels = trends.map((t: any) => t.period);
      this.reliabilityTrendChart = {
        series: [
          { name: 'Reliability', data: trends.map((t: any) => t.reliability_score) },
          { name: 'Delivery', data: trends.map((t: any) => t.delivery_score) },
          { name: 'Quality', data: trends.map((t: any) => t.quality_score) }
        ],
        chart: { type: 'line', height: 320, toolbar: { show: false }, fontFamily: 'inherit' },
        colors: ['#4f46e5', '#10b981', '#f59e0b'],
        stroke: { curve: 'smooth', width: 3 },
        markers: { size: 4 },
        xaxis: { categories: labels },
        yaxis: { min: 0, max: 100, labels: { formatter: (v: number) => `${Math.round(v)}` } },
        legend: { position: 'bottom' },
        dataLabels: { enabled: false }
      };
    }

    const d = res?.dashboard || {};
    this.subScoreChart = {
      series: [{
        name: 'Score',
        data: [
          d.delivery_score || 0,
          d.quality_score || 0,
          d.communication_score || 0,
          d.service_score || 0,
          res?.reliability?.reliability_score || 0
        ]
      }],
      chart: { type: 'bar', height: 320, toolbar: { show: false }, fontFamily: 'inherit' },
      colors: ['#6366f1'],
      plotOptions: { bar: { borderRadius: 6, distributed: true, columnWidth: '50%' } },
      dataLabels: { enabled: true, formatter: (v: number) => `${Math.round(v)}` },
      xaxis: { categories: ['Delivery', 'Quality', 'Communication', 'Service', 'Reliability'] },
      yaxis: { min: 0, max: 100 },
      legend: { show: false }
    };

    const delivery = res?.delivery_breakdown || {};
    const deliveryLabels = Object.keys(delivery);
    this.hasDelivery = deliveryLabels.length > 0;
    if (this.hasDelivery) {
      this.deliveryChart = {
        series: deliveryLabels.map((k) => delivery[k]),
        chart: { type: 'donut', height: 320, fontFamily: 'inherit' },
        labels: deliveryLabels,
        colors: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#94a3b8', '#8b5cf6'],
        legend: { position: 'bottom' }
      };
    }

    const spend = res?.monthly_spend || [];
    this.hasSpend = spend.some((m: any) => (m.total_spending || 0) > 0);
    this.monthlySpendChart = {
      series: [{ name: 'Procurement Spend (₹)', data: spend.map((m: any) => m.total_spending || 0) }],
      chart: { type: 'area', height: 320, toolbar: { show: false }, fontFamily: 'inherit' },
      colors: ['#06b6d4'],
      stroke: { curve: 'smooth', width: 3 },
      fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.45, opacityTo: 0.05 } },
      xaxis: { categories: spend.map((m: any) => m.month) },
      yaxis: { labels: { formatter: (v: number) => `₹${(v / 1000).toFixed(0)}k` } },
      dataLabels: { enabled: false }
    };
  }
}
