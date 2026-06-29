import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-invoice-management',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './invoice-management.html',
  styleUrls: ['./invoice-management.css'],
})
export class InvoiceManagement implements OnInit {
  invoices: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';
  userRole: string = '';
  showUploadModal: boolean = false;
  uploading: boolean = false;
  uploadError: string = '';
  newInvoice = {
    invoiceNumber: '',
    poId: null as number | null,
    procurementId: null as number | null,
    vendorId: null as number | null,
    vendorName: '',
    invoiceAmount: 0,
    taxAmount: 0,
    dueDate: '',
    remarks: '',
    selectedFile: null as File | null
  };
  purchaseOrders: any[] = [];
  constructor(
    private procurementService: ProcurementService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}
  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    this.userRole = user?.role || '';
    this.loadInvoices();
    this.loadPurchaseOrders();
  }
  loadInvoices(): void {
    this.loading = true;
    this.errorMsg = '';
    this.procurementService.getAllInvoices().subscribe({
      next: (data) => {
        this.loading = false;
        if (Array.isArray(data)) {
          this.invoices = data;
        } else {
          this.invoices = [];
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load invoices', err);
        this.errorMsg = 'Failed to load invoices from server.';
      }
    });
  }
  loadPurchaseOrders(): void {
    this.procurementService.getAllPurchaseOrders().subscribe({
      next: (pos) => this.purchaseOrders = pos,
      error: () => this.purchaseOrders = []
    });
  }
  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' | 'info' {
    switch (status) {
      case 'Paid': return 'success';
      case 'Approved': return 'info';
      case 'Verified': return 'primary';
      case 'Pending': return 'warning';
      case 'Rejected': return 'danger';
      default: return 'default';
    }
  }
}

const PLACEHOLDER_INVOICE_MANAGEMENT_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderInvoiceManagement(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_INVOICE_MANAGEMENT_ROWS;
  }
  return rows.filter((row) => !!row);
}
