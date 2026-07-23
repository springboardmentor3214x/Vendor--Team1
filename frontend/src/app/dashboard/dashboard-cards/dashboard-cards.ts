import { Component, OnInit } from '@angular/core';
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

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.http.get<VendorStats>('/vendors/stats').subscribe({
      next: (data) => {
        this.stats = data;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }
}