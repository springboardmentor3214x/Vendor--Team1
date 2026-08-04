import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';
import { InvoiceService } from '../../core/services/invoice.service';

@Component({
  selector: 'app-payment-details',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, InputComponent, Table],
  templateUrl: './payment-details.html',
  styleUrls: ['./payment-details.css']
})
export class PaymentDetails implements OnInit {
  loading: boolean = false;
  payments: any[] = [];
  loadError: string = '';

  showTransferModal: boolean = false;
  selectedPaymentId: number | null = null;
  transferRemarks: string = '';
  submitting: boolean = false;
  transferError: string = '';

  constructor(private invoiceService: InvoiceService) {}

  ngOnInit(): void {
    this.loadPayments();
  }

  loadPayments(): void {
    this.loading = true;
    this.loadError = '';
    this.invoiceService.getInvoices().subscribe({
      next: (invoices) => {
        this.loading = false;
        if (invoices && invoices.length > 0) {
          this.payments = invoices.map(i => ({
            id: `TXN-${1000 + i.id}`,
            invoiceId: i.id,
            invoice: i.invoice_number,
            vendor: i.vendor_name,
            amount: i.total_amount || i.invoice_amount,
            date: i.due_date ? new Date(i.due_date).toLocaleDateString() : 'N/A',
            status: i.payment_status || 'Pending'
          }));
        } else {
          this.payments = [];
        }
      },
      error: () => {
        this.loading = false;
        this.payments = [];
        this.loadError = 'Could not load payments. Please try again.';
      }
    });
  }

  get payablePayments(): any[] {
    return this.payments.filter(p => p.status === 'Verified' || p.status === 'Approved');
  }

  openTransferModal(): void {
    this.transferError = '';
    this.transferRemarks = '';
    this.selectedPaymentId = this.payablePayments.length
      ? this.payablePayments[0].invoiceId
      : null;
    this.showTransferModal = true;
  }

  closeTransferModal(): void {
    this.showTransferModal = false;
    this.submitting = false;
  }

  confirmTransfer(): void {
    if (!this.selectedPaymentId) {
      this.transferError = 'Select an invoice to pay.';
      return;
    }
    this.submitting = true;
    this.transferError = '';
    this.invoiceService.updatePaymentStatus(String(this.selectedPaymentId), 'Paid').subscribe({
      next: () => {
        this.submitting = false;
        this.showTransferModal = false;
        this.loadPayments();
      },
      error: (err) => {
        this.submitting = false;
        this.transferError = err?.error?.detail || 'Transfer failed. Please try again.';
      }
    });
  }

  receipt(): void {
    window.print();
  }
}