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

  loadPO(id: string): void {
    this.isLoading = true;
    this.procurementService.getPurchaseOrderById(id).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.po = res;
        this.selectedStatus = res.status || 'Issued';
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error fetching PO details', err);
        this.po = null;
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' {
    if (status === 'Completed' || status === 'Delivered') return 'success';
    if (status === 'Issued' || status === 'In Transit') return 'primary';
    if (status === 'Pending') return 'warning';
    if (status === 'Cancelled') return 'danger';
    return 'default';
  }

  updateStatus(): void {
    if (!this.poId || !this.selectedStatus) return;
    if (confirm(`Update Purchase Order status to '${this.selectedStatus}'?`)) {
      this.procurementService.updatePOStatus(this.poId, this.selectedStatus).subscribe({
        next: (res) => {
          alert(`Status updated to ${res.status || this.selectedStatus}`);
          this.loadPO(this.poId!);
        },
        error: (err) => alert('Failed to update status: ' + (err.error?.detail || err.message))
      });
    }
  }

  printPO(): void {
    window.print();
  }

  downloadPDF(): void {
    if (!this.poId) {
      return;
    }

    this.procurementService.downloadPurchaseOrderPdf(this.poId).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${this.po?.po_number || 'purchase-order'}.pdf`;
        link.click();
        setTimeout(() => URL.revokeObjectURL(url), 60000);
      },
      error: () => {
        this.errorMsg = 'The purchase order PDF could not be generated.';
      }
    });
  }
}
