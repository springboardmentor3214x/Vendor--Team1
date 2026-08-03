import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-vendor-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './vendor-dashboard.html',
  styleUrls: ['./vendor-dashboard.css']
})
export class VendorDashboard implements OnInit {
  reliabilityScore: string = '85.0 ⭐';
  activeOrdersCount: number = 0;
  unreadMessagesCount: number = 0;
  pendingContractsCount: number = 0;
  loading: boolean = true;
  recentActivities: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;

    // Load Procurements
    this.http.get<any[]>('/procurements/').subscribe({
      next: (orders) => {
        if (Array.isArray(orders)) {
          this.activeOrdersCount = orders.filter(o => o.status !== 'Completed' && o.status !== 'Cancelled').length;
          this.recentActivities = orders.slice(0, 5).map(o => ({
            date: o.created_at ? o.created_at.slice(0, 10) : '2026-07-30',
            activity: 'Purchase Order #' + o.id + ' (' + o.item_name + ')',
            status: o.status || 'Pending'
          }));
        }
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });

    // Load Contracts
    this.http.get<any[]>('/contracts/').subscribe({
      next: (contracts) => {
        if (Array.isArray(contracts)) {
          this.pendingContractsCount = contracts.filter(c => c.status === 'Pending').length;
        }
      }
    });

    // Load Communications
    this.http.get<any[]>('/communications/').subscribe({
      next: (comms) => {
        if (Array.isArray(comms)) {
          this.unreadMessagesCount = comms.length;
        }
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'info' | 'default' | 'danger' {
    if (status === 'Completed' || status === 'Delivered') return 'success';
    if (status === 'Pending') return 'warning';
    if (status === 'Dispatched' || status === 'Order Placed' || status === 'Approved') return 'info';
    return 'default';
  }

  refresh(): void {
    this.loadDashboardData();
  }
}