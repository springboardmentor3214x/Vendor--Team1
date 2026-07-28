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
}

const PLACEHOLDER_VENDOR_PERFORMANCE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorPerformance(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_PERFORMANCE_ROWS;
}
