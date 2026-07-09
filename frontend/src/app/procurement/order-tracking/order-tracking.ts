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
}

const PLACEHOLDER_ORDER_TRACKING_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderOrderTracking(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_ORDER_TRACKING_ROWS;
  }
  return rows.filter((row) => !!row);
}
