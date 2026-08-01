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
  vendorFilter = 'All';
  statusFilter = 'All';
  vendorNames: string[] = [];
}

const PLACEHOLDER_DELIVERY_PERFORMANCE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderDeliveryPerformance(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_DELIVERY_PERFORMANCE_ROWS;
  }
  return rows.filter((row) => !!row);
}
