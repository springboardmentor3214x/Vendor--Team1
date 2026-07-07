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

  openUploadModal(): void {
    this.showUploadModal = true;
    this.uploadError = '';
    this.newInvoice = {
      invoiceNumber: `INV-${Date.now().toString().slice(-6)}`,
      poId: null,
      procurementId: null,
      vendorId: null,
      vendorName: '',
      invoiceAmount: 0,
      taxAmount: 0,
      dueDate: new Date(Date.now() + 15 * 86400000).toISOString().slice(0, 10),
      remarks: '',
      selectedFile: null
    };
  }

  closeUploadModal(): void {
    this.showUploadModal = false;
  }

  onPoSelected(): void {
    if (this.newInvoice.poId) {
      const selected = this.purchaseOrders.find(po => po.id === Number(this.newInvoice.poId));
      if (selected) {
        this.newInvoice.procurementId = selected.procurement_id;
        this.newInvoice.vendorId = selected.vendor_id;
        this.newInvoice.vendorName = selected.vendor_name;
        this.newInvoice.invoiceAmount = selected.total_cost || (selected.quantity * selected.unit_price);
        this.newInvoice.taxAmount = selected.tax_amount || 0;
      }
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.newInvoice.selectedFile = input.files[0];
    }
  }

  submitInvoice(): void {
    if (!this.newInvoice.invoiceNumber || !this.newInvoice.poId || !this.newInvoice.invoiceAmount) {
      this.uploadError = 'Please fill out all mandatory invoice fields.';
      return;
    }

    this.uploading = true;
    this.uploadError = '';

    const formData = new FormData();
    formData.append('invoice_number', this.newInvoice.invoiceNumber);
    formData.append('po_id', String(this.newInvoice.poId));
    formData.append('procurement_id', String(this.newInvoice.procurementId || 0));
    formData.append('vendor_id', String(this.newInvoice.vendorId || 0));
    formData.append('vendor_name', this.newInvoice.vendorName || 'Vendor');
    formData.append('invoice_amount', String(this.newInvoice.invoiceAmount));
    formData.append('tax_amount', String(this.newInvoice.taxAmount || 0));
    if (this.newInvoice.remarks) formData.append('remarks', this.newInvoice.remarks);
    if (this.newInvoice.selectedFile) {
      formData.append('file', this.newInvoice.selectedFile, this.newInvoice.selectedFile.name);
    }

    this.procurementService.uploadInvoice(formData).subscribe({
      next: () => {
        this.uploading = false;
        alert('Invoice uploaded successfully!');
        this.closeUploadModal();
        this.loadInvoices();
      },
      error: (err) => {
        this.uploading = false;
        this.uploadError = err.error?.detail || 'Failed to upload invoice.';
      }
    });
  }

  verifyInvoice(inv: any): void {
    if (confirm(`Verify Invoice ${inv.invoice_number}?`)) {
      this.procurementService.verifyInvoice(inv.id, 'verify', 'Verified by Finance Officer').subscribe({
        next: () => {
          alert(`Invoice ${inv.invoice_number} Verified!`);
          this.loadInvoices();
        },
        error: (err) => alert('Verification failed: ' + (err.error?.detail || err.message))
      });
    }
  }

  approvePayment(inv: any): void {
    if (confirm(`Approve payment of $${inv.total_amount || inv.invoice_amount} for Invoice ${inv.invoice_number}? This will mark procurement as Completed.`)) {
      this.procurementService.verifyInvoice(inv.id, 'pay', 'Payment approved by Finance Officer').subscribe({
        next: () => {
          alert(`Payment for Invoice ${inv.invoice_number} Approved and Processed!`);
          this.loadInvoices();
        },
        error: (err) => alert('Payment approval failed: ' + (err.error?.detail || err.message))
      });
    }
  }

  rejectInvoice(inv: any): void {
    const reason = prompt('Please enter reason for rejecting this invoice:');
    if (reason !== null) {
      this.procurementService.verifyInvoice(inv.id, 'reject', reason || 'Invoice Rejected').subscribe({
        next: () => {
          alert(`Invoice ${inv.invoice_number} Rejected.`);
          this.loadInvoices();
        },
        error: (err) => alert('Rejection failed: ' + (err.error?.detail || err.message))
      });
    }
  }

  isFinanceOfficer(): boolean {
    return ['Administrator', 'Finance Officer'].includes(this.userRole);
  }
}
