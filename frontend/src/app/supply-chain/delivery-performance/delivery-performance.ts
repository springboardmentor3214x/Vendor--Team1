import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { forkJoin, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

import { PerformanceService } from '../../core/services/performance.service';
import { VendorService } from '../../services/vendor';

@Component({
  selector: 'app-delivery-performance',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button, Table],
  templateUrl: './delivery-performance.html',
  styleUrls: ['./delivery-performance.css']
})
export class DeliveryPerformance implements OnInit {
  allRecords: any[] = [];
  records: any[] = [];
  dashboard: any = {};
  isLoading = true;
  errorMsg = '';
}

const PLACEHOLDER_DELIVERY_PERFORMANCE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderDeliveryPerformance(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_DELIVERY_PERFORMANCE_ROWS;
}
