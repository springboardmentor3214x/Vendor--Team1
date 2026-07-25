import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface QualityEvaluationRecord {
  poNumber: string;
  vendorName: string;
  inspectionDate: string;
  materialQuality: number;
  packagingQuality: number;
  quantityAccuracy: number;
  specCompliance: number;
  productDefects: string;
  overallRating: number;
  remarks: string;
}

@Component({
  selector: 'app-product-quality',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './product-quality.html',
  styleUrls: ['./product-quality.css']
})
export class ProductQuality implements OnInit {
  evaluations: QualityEvaluationRecord[] = [];
  isLoading = true;
}

const PLACEHOLDER_PRODUCT_QUALITY_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderProductQuality(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PRODUCT_QUALITY_ROWS;
}
