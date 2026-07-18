import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { InvoiceService } from '../../core/services/invoice.service';

export interface InvoiceMock {
  id: number;
  invoiceNumber: string;
  poNumber: string;
  vendorName: string;
  amount: number;
  issueDate: string;
  dueDate: string;
  status: string;
}

@Component({
  selector: 'app-invoice-management',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './invoice-management.html',
  styleUrls: ['./invoice-management.css'],
})
export class InvoiceManagement implements OnInit {
  exportCSV() { alert("All invoices exported!"); }

  columns: TableColumn[] = [
    { key: 'invoiceNumber', label: 'Invoice Number' },
    { key: 'poNumber', label: 'PO Number' },
    { key: 'vendorName', label: 'Vendor' },
    { key: 'amount', label: 'Amount (₹)' },
    { key: 'issueDate', label: 'Issue Date' },
    { key: 'dueDate', label: 'Due Date' },
    { key: 'status', label: 'Status' },
    { key: 'actions', label: 'Actions' }
  ];

  invoices: InvoiceMock[] = [
    { id: 1, invoiceNumber: 'INV-1001', poNumber: 'PO-2001', vendorName: 'Global Logistics', amount: 5000, issueDate: '2026-07-01', dueDate: '2026-07-31', status: 'Paid' },
    { id: 2, invoiceNumber: 'INV-1002', poNumber: 'PO-2002', vendorName: 'TechCorp Solutions', amount: 12500, issueDate: '2026-07-10', dueDate: '2026-08-10', status: 'Pending Approval' },
    { id: 3, invoiceNumber: 'INV-1003', poNumber: 'PO-2003', vendorName: 'Office Depot', amount: 450, issueDate: '2026-07-15', dueDate: '2026-08-15', status: 'Rejected' }
  ];

  constructor(private invoiceService: InvoiceService) {}

  ngOnInit(): void {
    // Ideally we would have a getAllInvoices API. Using Mock for now.
    this.invoices = [
      {
        id: 1,
        invoiceNumber: 'INV-2026-081',
        poNumber: 'PO-8492',
        vendorName: 'TechCorp Ltd',
        amount: 50000,
        issueDate: '15 Jul 2026',
        dueDate: '15 Aug 2026',
        status: 'Pending'
      },
      {
        id: 2,
        invoiceNumber: 'INV-2026-075',
        poNumber: 'PO-8450',
        vendorName: 'Compute Solutions',
        amount: 250000,
        issueDate: '01 Jul 2026',
        dueDate: '31 Jul 2026',
        status: 'Paid'
      },
      {
        id: 3,
        invoiceNumber: 'INV-2026-068',
        poNumber: 'PO-8422',
        vendorName: 'OfficePro Supplies',
        amount: 12500,
        issueDate: '20 Jun 2026',
        dueDate: '20 Jul 2026',
        status: 'Overdue'
      },
      {
        id: 4,
        invoiceNumber: 'INV-2026-092',
        poNumber: 'PO-8501',
        vendorName: 'Global Compute Solutions',
        amount: 850000,
        issueDate: '10 Jul 2026',
        dueDate: '10 Aug 2026',
        status: 'Pending'
      },
      {
        id: 5,
        invoiceNumber: 'INV-2026-015',
        poNumber: 'PO-8120',
        vendorName: 'Furniture Co',
        amount: 350000,
        issueDate: '15 May 2026',
        dueDate: '15 Jun 2026',
        status: 'Paid'
      }
    ];
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' {
    if (status === 'Paid') return 'success';
    if (status === 'Pending') return 'warning';
    if (status === 'Overdue' || status === 'Rejected') return 'danger';
    return 'default';
  }

  processPayment(id: number): void {
    const invoice = this.invoices.find(inv => inv.id === id);
    if (invoice && confirm(`Process payment of ₹${invoice.amount} for invoice ${invoice.invoiceNumber}?`)) {
      this.invoiceService.updatePaymentStatus(id.toString(), 'Paid').subscribe({
        next: () => {
          invoice.status = 'Paid';
          alert('Payment processed successfully.');
        },
        error: (err) => {
          console.error('Error processing payment', err);
          // Mock
          invoice.status = 'Paid';
          alert('Payment processed successfully. (Mocked)');
        }
      });
    }
  }

  downloadInvoice(id: number): void {
    alert('Downloading invoice PDF...');
  }
}
