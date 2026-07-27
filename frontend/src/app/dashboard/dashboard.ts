import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

import { DashboardCards } from './dashboard-cards/dashboard-cards';
import { Card } from '../ui/card/card';
import { Badge } from '../ui/badge/badge';
import { Button } from '../ui/button/button';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    DashboardCards,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard implements OnInit {

  recentVendors: any[] = [];
  loadingRecent: boolean = true;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadRecentVendors();
  }

  loadRecentVendors(): void {
    this.loadingRecent = true;
    this.http.get<any[]>('/vendors/recent?limit=5').subscribe({
      next: (vendors) => {
        this.loadingRecent = false;
        if (Array.isArray(vendors)) {
          this.recentVendors = vendors.map(v => ({
            id: v.id,
            companyName: v.company_name,
            category: v.category,
            reliabilityScore: v.reliability_score
              ? v.reliability_score.toFixed(1) + ' ⭐'
              : '85.0 ⭐',
            status: v.status || 'Active'
          }));
        } else {
          this.recentVendors = [];
        }
      },
      error: (err) => {
        this.loadingRecent = false;
        console.error('Failed to load recent vendors', err);
      }
    });
  }

  refresh() {
    this.loadRecentVendors();
  }
}