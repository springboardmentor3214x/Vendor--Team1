import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface VendorStats {
  total: number;
  approved: number;
  pending_review: number;
  suspended: number;
  rejected: number;
  high_risk: number;
}

@Component({
  selector: 'app-dashboard-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-cards.html',
  styleUrl: './dashboard-cards.css'
})
export class DashboardCards implements OnInit {

  stats: VendorStats = {
    total: 0,
    approved: 0,
    pending_review: 0,
    suspended: 0,
    rejected: 0,
    high_risk: 0
  };

  loading = true;
  errorMsg = '';

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.loading = true;
    this.errorMsg = '';
    this.http.get<VendorStats>('/vendors/stats').subscribe({
      next: (data) => {
        if (data) {
          this.stats = {
            total: data.total ?? 0,
            approved: data.approved ?? 0,
            pending_review: data.pending_review ?? 0,
            suspended: data.suspended ?? 0,
            rejected: data.rejected ?? 0,
            high_risk: data.high_risk ?? 0
          };
        }
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error) => {
        this.loading = false;
        this.cdr.markForCheck();
        this.errorMsg = error.error?.detail || 'Could not load vendor totals.';
      }
    });
  }
}
