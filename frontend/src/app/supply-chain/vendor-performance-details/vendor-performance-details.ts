import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface HistoryRow {
  poNumber: string;
  requestNumber: string;
  itemName: string;
  date: string | null;
  deliveryStatus: string;
  delayDays: number | null;
  qualityRating: number | null;
  serviceRating: number | null;
}

@Component({
  selector: 'app-vendor-performance-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './vendor-performance-details.html',
  styleUrls: ['./vendor-performance-details.css']
})
export class VendorPerformanceDetails implements OnInit {
  vendorId: string = '';
  isLoading = true;
  errorMsg = '';

  vendor: any = {
    id: '',
    name: 'Loading…',
    category: '',
    rating: 0,
    score: '0.0'
  };

  metrics: any = {};
  history: HistoryRow[] = [];

  constructor(
    private route: ActivatedRoute,
    private performanceService: PerformanceService
  ) {}

  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id') || '';
    if (!this.vendorId) {
      this.isLoading = false;
      this.errorMsg = 'No vendor was specified.';
      return;
    }
    this.loadVendorPerformance(this.vendorId);
  }

  loadVendorPerformance(id: string) {
    this.isLoading = true;
    this.errorMsg = '';

    this.performanceService.getVendorHistory(id).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (!res || !res.current_metrics) {
          this.errorMsg = 'No performance data is available for this vendor.';
          return;
        }

        const m = res.current_metrics;
        this.metrics = m;
        this.vendor = {
          id: res.vendor_id,
          name: res.company_name || res.vendor_name || `Vendor #${res.vendor_id}`,
          category: res.category || '—',
          status: res.status,
          rating: Math.round((m.overall_performance_score || 0) / 20),
          score: ((m.overall_performance_score || 0) / 20).toFixed(1)
        };

        this.history = this.buildHistory(res);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = err.error?.detail || 'Could not load this vendor’s performance history.';
      }
    });
  }

  private buildHistory(res: any): HistoryRow[] {
    const rows = new Map<number, HistoryRow>();

    const rowFor = (rec: any): HistoryRow => {
      const key = rec.procurement_id;
      if (!rows.has(key)) {
        rows.set(key, {
          poNumber: rec.po_number || '—',
          requestNumber: rec.request_number || '—',
          itemName: rec.item_name || '—',
          date: null,
          deliveryStatus: '—',
          delayDays: null,
          qualityRating: null,
          serviceRating: null
        });
      }
      return rows.get(key)!;
    };

    for (const d of res.delivery_records || []) {
      const row = rowFor(d);
      row.deliveryStatus = d.status || '—';
      row.delayDays = d.delay_days ?? null;
      row.date = d.actual_date || d.recorded_at || row.date;
    }

    for (const q of res.quality_evaluations || []) {
      const row = rowFor(q);
      row.qualityRating = q.overall_rating ?? null;
      row.date = row.date || q.inspection_date;
    }

    for (const s of res.service_ratings || []) {
      const row = rowFor(s);
      row.serviceRating = s.overall_rating ?? null;
      row.date = row.date || s.rated_at;
    }

    for (const c of res.communication_logs || []) {
      rowFor(c);
    }

    return Array.from(rows.values()).sort((a, b) => {
      const left = a.date ? new Date(a.date).getTime() : 0;
      const right = b.date ? new Date(b.date).getTime() : 0;
      return right - left;
    });
  }

  isOnTime(status: string): boolean {
    return status === 'Delivered On Time' || status === 'Delivered Early';
  }

  stars(rating: number | null): number {
    return Math.round(rating || 0);
  }
}
