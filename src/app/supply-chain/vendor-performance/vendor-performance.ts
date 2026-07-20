import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { NgApexchartsModule } from 'ng-apexcharts';

import {
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexDataLabels,
  ApexStroke,
  ApexYAxis,
  ApexTitleSubtitle,
  ApexLegend,
  ApexTooltip,
  ApexGrid
} from 'ng-apexcharts';

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  stroke: ApexStroke;
  dataLabels: ApexDataLabels;
  yaxis: ApexYAxis;
  title: ApexTitleSubtitle;
  legend: ApexLegend;
  tooltip: ApexTooltip;
  grid: ApexGrid;
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

  ngOnInit() {
    this.chartOptions = {
      series: [
        {
          name: 'Delivery Score',
          data: [85, 87, 88, 90, 92, 94, 95]
        },
        {
          name: 'Quality Score',
          data: [90, 89, 92, 91, 95, 96, 98]
        }
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
        text: 'Average Vendor Performance Trends (Last 7 Months)',
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
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
      },
      yaxis: {
        min: 60,
        max: 100
      },
      legend: {
        position: 'top',
        horizontalAlign: 'right'
      }
    };
  }

  viewDetails(v: any) { alert("Viewing details for " + v.name); }

  filter() { alert("Filter applied"); }

  topVendors = [
    { id: 'VND-001', name: 'TechCorp Solutions', category: 'IT Equipment', rating: 5, onTime: '99%', score: '4.9' },
    { id: 'VND-002', name: 'Global Logistics Inc.', category: 'Services', rating: 4, onTime: '94%', score: '4.5' },
    { id: 'VND-003', name: 'Prime Raw Materials', category: 'Raw Materials', rating: 4, onTime: '95%', score: '4.2' },
    { id: 'VND-004', name: 'Office Depot', category: 'Office Supplies', rating: 3, onTime: '88%', score: '3.9' }
  ];
}