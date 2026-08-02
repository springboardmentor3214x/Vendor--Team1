import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface ServiceRecord {
  poNumber: string;
  vendorName: string;
  professionalism: number;
  customerSupport: number;
  documentationQuality: number;
  flexibility: number;
  communicationEffectiveness: number;
  issueResolution: number;
  overallRating: number;
  comments: string;
}

@Component({
  selector: 'app-service-rating',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './service-rating.html',
  styleUrls: ['./service-rating.css']
})
export class ServiceRating implements OnInit {
  ratings: ServiceRecord[] = [];
  isLoading = true;
  constructor(private performanceService: PerformanceService) {}
  ngOnInit() {
    this.loadRatings();
  }
}

const PLACEHOLDER_SERVICE_RATING_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 6, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 7, name: 'Northwind Steel', status: 'Active' },
  { id: 8, name: 'Orbit IT Systems', status: 'Pending Approval' },
];

function usePlaceholderServiceRating(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_SERVICE_RATING_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
