import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-finance-purchase-orders',
  standalone: true,
  imports: [CommonModule, Card, Button, Badge],
  templateUrl: './finance-purchase-orders.html',
  styleUrls: ['./finance-purchase-orders.css']
})
export class FinancePurchaseOrders implements OnInit {
  orders: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';
}

const PLACEHOLDER_FINANCE_PURCHASE_ORDERS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderFinancePurchaseOrders(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_FINANCE_PURCHASE_ORDERS_ROWS;
}
