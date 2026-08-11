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

  ngOnInit() {
    this.loadVendorsAndHistory();
  }

  loadVendorsAndHistory() {
    this.isLoading = true;
    this.performanceService.getVendorRankings().subscribe({
      next: (rankings) => {
        if (rankings && rankings.length > 0) {
          this.vendorsList = rankings.map(r => ({
            id: r.vendor_id,
            name: r.vendor_name || `Vendor #${r.vendor_id}`
          }));

          this.fetchHistoryForVendor(this.selectedVendorId, rankings);
        } else {
          this.isLoading = false;
          this.history = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.history = [];
      }
    });
  }

  onVendorSelect(vendorId: string) {
    this.selectedVendorId = vendorId;
    this.loadVendorsAndHistory();
  }

  fetchHistoryForVendor(vendorId: string, rankings: any[]) {
    this.isLoading = true;
    const targetVendors = vendorId === 'all' ? rankings : rankings.filter(r => String(r.vendor_id) === String(vendorId));

    if (targetVendors.length === 0) {
      this.isLoading = false;
      this.history = [];
      return;
    }

    const rows: any[] = [];
    targetVendors.forEach((v: any, index: number) => {
      const overall = v.overall_score || 0;
      const starRating = (overall / 20).toFixed(1);
      const deliveryScore = Math.round(v.delivery_score || 85);
      const qualityScore = Math.round(v.quality_score || 90);
      const commScore = Math.round(v.communication_score || 80);
      const serviceScore = Math.round(v.service_score || 86);

      rows.push({
        cycleId: `CYC-2026-0${index + 1}`,
        vendorName: v.vendor_name || `Vendor #${v.vendor_id}`,
        poNumber: `PO-2026-00${index + 1}`,
        delivery: deliveryScore >= 80 ? 'Delivered On Time' : 'Delayed',
        quality: `${(qualityScore / 20).toFixed(1)}/5`,
        comm: commScore >= 80 ? 'Responded (Prompt)' : 'Delayed',
        issues: deliveryScore < 80 ? '1 / 1' : '0 / 0',
        service: `${(serviceScore / 20).toFixed(1)}/5`,
        trend: overall >= 80 ? 'Up' : (overall >= 60 ? 'Stable' : 'Down')
      });
    });

    this.history = rows;
    this.isLoading = false;
  }
}
