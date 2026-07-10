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
}

const PLACEHOLDER_PURCHASE_ORDER_DETAILS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderPurchaseOrderDetails(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PURCHASE_ORDER_DETAILS_ROWS;
}
