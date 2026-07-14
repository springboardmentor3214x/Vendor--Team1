import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-purchase-order-details',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './purchase-order-details.html',
  styleUrls: ['./purchase-order-details.css'],
})
export class PurchaseOrderDetails implements OnInit {
  poId: string | null = null;
  po: any = null;
  isLoading = true;
  selectedStatus = '';
  errorMsg = '';
  statusOptions = ['Issued', 'In Transit', 'Delivered', 'Completed', 'Cancelled'];
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private procurementService: ProcurementService
  ) {}
  ngOnInit(): void {
    this.poId = this.route.snapshot.paramMap.get('id');
    if (this.poId) {
      this.loadPO(this.poId);
    }
  }
}

const PLACEHOLDER_PURCHASE_ORDER_DETAILS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderPurchaseOrderDetails(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PURCHASE_ORDER_DETAILS_ROWS;
  }
  return rows.filter((row) => !!row);
}
