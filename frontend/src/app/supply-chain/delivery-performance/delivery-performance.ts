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

  private toRow(r: any, vendorName: string): any {
    const delay = r.delay_days ?? 0;
    return {
      recordId: r.id,
      procurementId: r.procurement_id,
      vendorName,
      expectedDate: this.fmt(r.expected_date),
      actualDate: this.fmt(r.actual_date),
      actualDateRaw: r.actual_date || '',
      delayDays: delay,
      status: r.delivery_status || '-',
      remarks: r.remarks || '-'
    };
  }

  private fmt(value: string): string {
    if (!value) return '-';
    const d = new Date(value);
    return isNaN(d.getTime()) ? '-' : d.toLocaleDateString();
  }

  applyFilters(): void {
    this.records = this.allRecords.filter(r => {
      const vendorOk = this.vendorFilter === 'All' || r.vendorName === this.vendorFilter;
      let statusOk = true;
      if (this.statusFilter === 'On Time') statusOk = r.status.includes('On Time');
      else if (this.statusFilter === 'Early') statusOk = r.status.includes('Early');
      else if (this.statusFilter === 'Delayed') statusOk = r.status.includes('Delayed');
      return vendorOk && statusOk;
    });
  }

  getStatusColor(status: string): string {
    if (status.includes('On Time') || status.includes('Early')) return '#34c759';
    if (status.includes('Delayed')) return '#ff3b30';
    return '#8e8e93';
  }
}
