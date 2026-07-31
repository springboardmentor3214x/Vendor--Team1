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
}

const PLACEHOLDER_SERVICE_RATING_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderServiceRating(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_SERVICE_RATING_ROWS;
  }
  return rows.filter((row) => !!row);
}
