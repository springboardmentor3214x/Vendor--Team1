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
  constructor(
    private performanceService: PerformanceService,
    private vendorService: VendorService
  ) {}
  ngOnInit(): void {
    this.performanceService.getDashboardStats().subscribe({
      next: (data) => this.dashboard = data || {},
      error: () => this.dashboard = {}
    });
    this.loadDeliveryRecords();
  }
  loadDeliveryRecords(): void {
    this.isLoading = true;
    this.errorMsg = '';

    this.vendorService.loadVendors().subscribe({
      next: (vendors) => {
        const approved = (vendors || []).filter(v => v.approvalStatus === 'Approved');
        this.vendorNames = approved.map(v => v.companyName).sort();

        if (approved.length === 0) {
          this.isLoading = false;
          this.allRecords = [];
          this.records = [];
          return;
        }

        forkJoin(
          approved.map(v =>
            this.performanceService.getDeliveryRecords(v.id).pipe(
              map(rows => (rows || []).map(r => this.toRow(r, v.companyName))),
              catchError(() => of([] as any[]))
            )
          )
        ).subscribe({
          next: (grouped) => {
            this.isLoading = false;
            this.allRecords = grouped
              .flat()
              .sort((a, b) => (b.actualDateRaw || '').localeCompare(a.actualDateRaw || ''));
            this.applyFilters();
          },
          error: () => {
            this.isLoading = false;
            this.errorMsg = 'Could not load delivery records.';
          }
        });
      },
      error: () => {
        this.isLoading = false;
        this.errorMsg = 'Could not load vendors.';
      }
    });
  }
}

const PLACEHOLDER_DELIVERY_PERFORMANCE_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 6, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 7, name: 'Northwind Steel', status: 'Active' },
  { id: 8, name: 'Orbit IT Systems', status: 'Pending Approval' },
];

function usePlaceholderDeliveryPerformance(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_DELIVERY_PERFORMANCE_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
