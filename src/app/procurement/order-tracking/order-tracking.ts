import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { PurchaseOrderService } from '../../core/services/purchase-order.service';

export interface TrackingEvent {
  status: string;
  location: string;
  date: string;
  completed: boolean;
}

@Component({
  selector: 'app-order-tracking',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './order-tracking.html',
  styleUrls: ['./order-tracking.css'],
})
export class OrderTracking implements OnInit {
  poId: string | null = null;
  isDelayed = false;
  
  trackingData = {
    carrier: 'BlueDart Logistics',
    trackingNumber: 'BDL-9988776655',
    estimatedDelivery: '20 Jul 2026',
    shippingMethod: 'Express Freight',
    origin: 'TechCorp Warehouse, Mumbai',
    destination: 'HQ Warehouse, Tech City, Bangalore'
  };

  events: TrackingEvent[] = [
    {
      status: 'Delivered',
      location: 'HQ Warehouse, Tech City, Bangalore',
      date: 'Pending',
      completed: false
    },
    {
      status: 'Out for Delivery',
      location: 'Bangalore Hub',
      date: 'Pending',
      completed: false
    },
    {
      status: 'In Transit',
      location: 'Pune Checkpoint',
      date: '18 Jul 2026, 04:30 AM',
      completed: true
    },
    {
      status: 'Dispatched',
      location: 'TechCorp Warehouse, Mumbai',
      date: '17 Jul 2026, 08:00 PM',
      completed: true
    },
    {
      status: 'Shipment Created',
      location: 'TechCorp Warehouse, Mumbai',
      date: '17 Jul 2026, 11:15 AM',
      completed: true
    }
  ];

  constructor(
    private route: ActivatedRoute,
    private poService: PurchaseOrderService
  ) {}

  ngOnInit(): void {
    this.poId = this.route.snapshot.paramMap.get('id');
    if (this.poId) {
      this.loadTrackingData(this.poId);
    }
  }

  loadTrackingData(id: string): void {
    this.poService.trackPurchaseOrder(id).subscribe({
      next: (res) => {
        // Assume API returns trackingData and events
        // this.trackingData = res.trackingData;
        // this.events = res.events;
        this.checkDelay();
      },
      error: (err) => {
        console.error('Error tracking', err);
        // Using mock data already present
        this.checkDelay();
      }
    });
  }

  checkDelay(): void {
    const today = new Date();
    today.setHours(0,0,0,0);
    const expected = new Date(this.trackingData.estimatedDelivery);
    // If today is strictly past the expected delivery date, it's delayed
    if (today > expected && !this.events[0].completed) { // events[0] is 'Delivered'
      this.isDelayed = true;
    }
  }

  printTracking(): void {
    window.print();
  }
}
