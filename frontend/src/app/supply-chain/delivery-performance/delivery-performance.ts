import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-delivery-performance',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './delivery-performance.html',
  styleUrls: ['./delivery-performance.css']
})
export class DeliveryPerformance implements OnInit {
  records: any[] = [];
  dashboard: any = {};

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any>('/performance/dashboard').subscribe({
      next: (data) => {
        this.dashboard = data;
      }
    });
    this.http.get<any[]>('/performance/rankings').subscribe({
      next: (rankings) => {
        this.records = rankings.map(r => ({
          poNumber: `V-${r.vendor_id}`,
          vendorName: r.vendor_name,
          expectedDate: '-',
          actualDate: '-',
          delayDays: 0,
          status: r.delivery_score >= 80 ? 'Delivered On Time' : 'Delayed 5-10 Hours',
          remarks: `Overall score ${r.overall_score}`
        }));
      }
    });
  }

  getStatusColor(status: string): string {
    if (status.includes('On Time') || status.includes('Early')) return '#34c759';
    if (status.includes('Delayed')) return '#ff3b30';
    return '#8e8e93';
  }
}
