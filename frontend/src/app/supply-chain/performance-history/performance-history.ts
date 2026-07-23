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
}

const PLACEHOLDER_PERFORMANCE_HISTORY_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderPerformanceHistory(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PERFORMANCE_HISTORY_ROWS;
}
