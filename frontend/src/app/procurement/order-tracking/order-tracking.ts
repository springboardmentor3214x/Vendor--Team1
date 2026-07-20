import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-order-tracking',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './order-tracking.html',
  styleUrls: ['./order-tracking.css'],
})
export class OrderTracking implements OnInit {
  poId: string | null = null;
  tracking: any = null;
  poDetails: any = null;
  isDelayed = false;
  isLoading = true;
  errorMessage = '';

  selectedStatus = '';
  deliveryStatuses = ['Awaiting Shipment', 'In Transit', 'Delivered', 'Delayed', 'Completed'];
  userRole = '';

  events: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private procurementService: ProcurementService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    this.userRole = user?.role || '';
    this.poId = this.route.snapshot.paramMap.get('id');
    if (this.poId) {
      this.loadTrackingData(this.poId);
    }
  }

  loadTrackingData(id: string): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.procurementService.getPurchaseOrderById(id).subscribe({
      next: (poRes) => {
        this.poDetails = poRes;
        this.procurementService.getOrderTrackingByPO(id).subscribe({
          next: (res) => {
            this.isLoading = false;
            this.tracking = res;
            this.selectedStatus = res.delivery_status || 'Awaiting Shipment';
            this.checkDelayStatus();
            this.buildTimelineEvents();
          },
          error: (err) => {
            this.isLoading = false;
            console.error('Error fetching tracking', err);
            this.errorMessage = 'No tracking record found for this Purchase Order yet.';
          }
        });
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Purchase Order not found.';
      }
    });
  }

  checkDelayStatus(): void {
    if (!this.tracking) return;
    const now = new Date();
    const expected = this.tracking.expected_delivery_date || this.poDetails?.expected_delivery_date;
    if (expected) {
      const expDate = new Date(expected);
      if (now > expDate && !['Delivered', 'Completed'].includes(this.tracking.delivery_status)) {
        this.isDelayed = true;
        this.tracking.delay_status = 'Delayed';
      } else {
        this.isDelayed = this.tracking.delay_status === 'Delayed';
      }
    }
  }

  buildTimelineEvents(): void {
    if (!this.tracking) return;
    const status = this.tracking.delivery_status;

    this.events = [
      {
        title: 'Order Completed & Payment Verified',
        location: 'Finance & Supply Chain',
        date: status === 'Completed' ? (this.tracking.updated_at ? new Date(this.tracking.updated_at).toLocaleString() : 'Done') : 'Pending',
        completed: status === 'Completed'
      },
      {
        title: 'Products Delivered',
        location: 'Destination Warehouse',
        date: this.tracking.actual_delivery_date ? new Date(this.tracking.actual_delivery_date).toLocaleString() : 'In Transit',
        completed: status === 'Delivered' || status === 'Completed'
      },
      {
        title: 'Dispatched & In Transit',
        location: 'Logistics Network',
        date: this.tracking.dispatch_date ? new Date(this.tracking.dispatch_date).toLocaleString() : 'Awaiting Dispatch',
        completed: status === 'In Transit' || status === 'Delivered' || status === 'Completed'
      },
      {
        title: 'Shipment Order Created',
        location: 'Supplier Facility',
        date: this.poDetails?.po_date ? new Date(this.poDetails.po_date).toLocaleString() : 'Confirmed',
        completed: true
      }
    ];
  }

  updateStatus(): void {
    if (!this.poId || !this.selectedStatus) return;
    const payload = {
      delivery_status: this.selectedStatus,
      dispatch_date: this.selectedStatus === 'In Transit' ? new Date().toISOString() : this.tracking?.dispatch_date,
      actual_delivery_date: (this.selectedStatus === 'Delivered' || this.selectedStatus === 'Completed') ? new Date().toISOString() : this.tracking?.actual_delivery_date
    };

    this.procurementService.updateOrderTracking(this.poId, payload).subscribe({
      next: (res) => {
        alert(`Order tracking status updated to '${res.delivery_status}'!`);
        this.loadTrackingData(this.poId!);
      },
      error: (err) => alert('Failed to update tracking: ' + (err.error?.detail || err.message))
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' | 'info' {
    switch (status) {
      case 'Delivered':
      case 'Completed': return 'success';
      case 'In Transit': return 'info';
      case 'Awaiting Shipment': return 'warning';
      case 'Delayed': return 'danger';
      default: return 'default';
    }
  }

  printTracking(): void {
    window.print();
  }
}
