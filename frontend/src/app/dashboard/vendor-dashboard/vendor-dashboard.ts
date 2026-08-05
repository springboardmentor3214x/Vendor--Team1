import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

import { VendorService } from '../../services/vendor';
import { ProcurementService } from '../../core/services/procurement.service';
import { ContractService } from '../../core/services/contract.service';
import { CommunicationService } from '../../core/services/communication.service';

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
  reliabilityScore: string = 'N/A';
  activeOrdersCount: number = 0;
  unreadMessagesCount: number = 0;
  pendingContractsCount: number = 0;
  loading: boolean = true;
  recentActivities: any[] = [];
  vendorProfile: any = null;

  constructor(
    private vendorService: VendorService,
    private procurementService: ProcurementService,
    private contractService: ContractService,
    private commService: CommunicationService
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;

    this.vendorService.getMyVendorProfile().subscribe({
      next: (v: any) => {
        if (v) {
          this.vendorProfile = v;
          const score = v.reliability_score ?? v.rating ?? 0.0;
          this.reliabilityScore = score.toFixed(1) + ' ⭐';
        } else {
          this.reliabilityScore = '0.0 ⭐';
        }
      },
      error: () => {
        this.reliabilityScore = '0.0 ⭐';
      }
    });

    this.procurementService.getAllProcurementRequests().subscribe({
      next: (orders) => {
        if (Array.isArray(orders)) {
          this.activeOrdersCount = orders.filter(o => o.status !== 'Completed' && o.status !== 'Cancelled').length;
          this.recentActivities = orders.slice(0, 5).map(o => ({
            date: o.created_at ? o.created_at.slice(0, 10) : new Date().toISOString().slice(0, 10),
            activity: 'Purchase Order #' + o.id + ' (' + o.item_name + ')',
            status: o.status || 'Pending'
          }));
        } else {
          this.activeOrdersCount = 0;
          this.recentActivities = [];
        }
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.activeOrdersCount = 0;
        this.recentActivities = [];
      }
    });

    this.contractService.getContracts().subscribe({
      next: (contracts) => {
        if (Array.isArray(contracts)) {
          this.pendingContractsCount = contracts.filter(c => c.status === 'Pending' || c.status === 'Draft').length;
        } else {
          this.pendingContractsCount = 0;
        }
      },
      error: () => {
        this.pendingContractsCount = 0;
      }
    });

    this.commService.getMessages().subscribe({
      next: (comms) => {
        if (Array.isArray(comms)) {
          this.unreadMessagesCount = comms.filter(m => !m.is_read).length;
        } else {
          this.unreadMessagesCount = 0;
        }
      },
      error: () => {
        this.unreadMessagesCount = 0;
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