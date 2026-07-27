import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table, TableColumn } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

@Component({
  selector: 'app-performance-history',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, Card, Button, Table],
  templateUrl: './performance-history.html',
  styleUrls: ['./performance-history.css']
})
export class PerformanceHistory implements OnInit {
  history: any[] = [];
  vendorsList: any[] = [];
  selectedVendorId: string = 'all';
  isLoading = true;
  columns: TableColumn[] = [
    { key: 'cycleId', label: 'Cycle ID' },
    { key: 'vendorName', label: 'Vendor Name' },
    { key: 'poNumber', label: 'PO Number' },
    { key: 'delivery', label: 'Delivery' },
    { key: 'quality', label: 'Quality' },
    { key: 'comm', label: 'Comm.' },
    { key: 'issues', label: 'Issues (R/Res)' },
    { key: 'service', label: 'Service' },
    { key: 'trend', label: 'Trend' }
  ];
  constructor(private performanceService: PerformanceService) {}
}

const PLACEHOLDER_PERFORMANCE_HISTORY_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderPerformanceHistory(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PERFORMANCE_HISTORY_ROWS;
  }
  return rows.filter((row) => !!row);
}
