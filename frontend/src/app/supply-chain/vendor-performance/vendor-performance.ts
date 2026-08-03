import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { NgApexchartsModule } from 'ng-apexcharts';
import { PerformanceService } from '../../core/services/performance.service';

export type ChartOptions = {
  series: any;
  chart: any;
  xaxis: any;
  stroke: any;
  dataLabels: any;
  yaxis: any;
  title: any;
  legend: any;
  tooltip: any;
  grid: any;
  colors: string[];
};

@Component({
  selector: 'app-vendor-performance',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table, NgApexchartsModule],
  templateUrl: './vendor-performance.html',
  styleUrls: ['./vendor-performance.css']
})
export class VendorPerformance implements OnInit {
  public chartOptions: Partial<ChartOptions> | any;
  topVendors: any[] = [];
  isLoading = true;

  totalEvaluated = 0;
  totalCompleted = 0;
  avgDeliveryPerf = '—';
  delayedDeliveries = 0;
  avgQuality = '—';
  avgResponseTime = '—';
  errorMsg = '';

  constructor(private performanceService: PerformanceService) {}

  ngOnInit() {
    this.initChart();
    this.loadDashboard();
    this.loadTopVendors();
  }

  loadDashboard() {
    this.performanceService.getDashboardStats().subscribe({
      next: (d) => {
        this.totalEvaluated = d.total_vendors_evaluated ?? 0;
        this.totalCompleted = d.total_completed_orders ?? 0;
        this.avgDeliveryPerf = `${d.avg_delivery_performance ?? 0}%`;
        this.delayedDeliveries = d.delayed_deliveries ?? 0;
        this.avgQuality = (d.avg_quality_rating ?? 0).toFixed(1);
        this.avgResponseTime = `${(d.avg_response_time_hours ?? 0).toFixed(1)} Hrs`;
      },
      error: () => {
        this.errorMsg = 'Could not load the performance summary.';
      }
    });
  }

  loadTopVendors() {
    this.isLoading = true;
    this.performanceService.getVendorRankings().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.length > 0) {
          this.topVendors = res.map((v: any) => ({

            id: v.vendor_id,
            name: v.company_name || v.vendor_name,
            category: v.category || 'General',
            rating: Math.round((v.overall_score || 0) / 20),
            onTime: `${Math.round(v.delivery_score || 0)}%`,
            qualityScore: ((v.quality_score || 0) / 20).toFixed(1),
            overallScore: ((v.overall_score || 0) / 20).toFixed(1),
            evaluated: v.evaluated
          }));

          const chartVendors = res.slice(0, 8);
          this.chartOptions.series = [
            { name: 'Delivery Score', data: chartVendors.map((v: any) => Math.round(v.delivery_score || 0)) },
            { name: 'Quality Score', data: chartVendors.map((v: any) => Math.round(v.quality_score || 0)) }
          ];
          this.chartOptions.xaxis.categories =
            chartVendors.map((v: any) => v.company_name || v.vendor_name || `Vendor #${v.vendor_id}`);
        } else {
          this.topVendors = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.topVendors = [];
        this.errorMsg = 'Could not load vendor rankings.';
      }
    });
  }

  initChart() {
    this.chartOptions = {

      series: [
        { name: 'Delivery Score', data: [] },
        { name: 'Quality Score', data: [] }
      ],
      chart: {
        height: 350,
        type: 'line',
        toolbar: { show: false },
        fontFamily: 'inherit'
      },
      colors: ['#3b82f6', '#34c759'],
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth',
        width: 3
      },
      title: {
        text: 'Delivery and Quality Scores by Vendor',
        align: 'left',
        style: {
          fontSize: '14px',
          fontWeight: 600,
          color: '#333'
        }
      },
      grid: {
        borderColor: '#f1f1f1',
      },
      xaxis: {
        categories: []
      },
      yaxis: {
        min: 0,
        max: 100
      },
      legend: {
        position: 'top',
        horizontalAlign: 'right'
      }
    };
  }

  filter() {
    this.loadDashboard();
    this.loadTopVendors();
  }
}