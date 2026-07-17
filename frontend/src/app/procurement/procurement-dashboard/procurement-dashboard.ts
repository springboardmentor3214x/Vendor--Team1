import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-procurement-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  templateUrl: './procurement-dashboard.html',
  styleUrl: './procurement-dashboard.css'
})
export class ProcurementDashboard implements OnInit {
  isLoading = true;
  summaryCards: any[] = [];
  recentActivities: any[] = [];

  constructor(private procurementService: ProcurementService) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.isLoading = true;
    this.procurementService.getProcurementDashboard().subscribe({
      next: (data) => {
        this.isLoading = false;
        this.summaryCards = [
          { title: 'Total Procurement Requests', value: data.total || 0, color: '#2563eb', icon: 'inventory_2' },
          { title: 'Pending Requests', value: data.pending || 0, color: '#f59e0b', icon: 'hourglass_empty' },
          { title: 'Approved Requests', value: data.approved || 0, color: '#16a34a', icon: 'task_alt' },
          { title: 'Purchase Orders Created', value: data.po_created || 0, color: '#9333ea', icon: 'receipt' },
          { title: 'Delivered Orders', value: data.delivered || 0, color: '#0f766e', icon: 'local_shipping' },
          { title: 'Completed Procurements', value: data.completed || 0, color: '#15803d', icon: 'verified' },
          { title: 'Cancelled Requests', value: data.cancelled || 0, color: '#dc2626', icon: 'cancel' }
        ];
        this.recentActivities = data.recent_activities || [];
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error fetching procurement dashboard data', err);

        this.summaryCards = [
          { title: 'Total Procurement Requests', value: 0, color: '#2563eb', icon: 'inventory_2' },
          { title: 'Pending Requests', value: 0, color: '#f59e0b', icon: 'hourglass_empty' },
          { title: 'Approved Requests', value: 0, color: '#16a34a', icon: 'task_alt' },
          { title: 'Purchase Orders Created', value: 0, color: '#9333ea', icon: 'receipt' },
          { title: 'Delivered Orders', value: 0, color: '#0f766e', icon: 'local_shipping' },
          { title: 'Completed Procurements', value: 0, color: '#15803d', icon: 'verified' },
          { title: 'Cancelled Requests', value: 0, color: '#dc2626', icon: 'cancel' }
        ];
      }
    });
  }
}