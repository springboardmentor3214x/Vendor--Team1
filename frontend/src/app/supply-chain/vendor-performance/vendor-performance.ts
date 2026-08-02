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
}

const PLACEHOLDER_VENDOR_PERFORMANCE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorPerformance(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_PERFORMANCE_ROWS;
  }
  return rows.filter((row) => !!row);
}
