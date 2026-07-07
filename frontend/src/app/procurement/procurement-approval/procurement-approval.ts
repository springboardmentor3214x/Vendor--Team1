import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-procurement-approval',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './procurement-approval.html',
  styleUrls: ['./procurement-approval.css'],
})
export class ProcurementApproval implements OnInit {
  request: any = null;
  requestId: string | null = null;
  remarks: string = '';
  isProcessing: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private procurementService: ProcurementService
  ) {}

  ngOnInit(): void {
    this.requestId = this.route.snapshot.paramMap.get('id');
    if (this.requestId) {
      this.loadRequest(this.requestId);
    }
  }

  loadRequest(id: string): void {
    this.procurementService.getProcurementRequestById(id).subscribe({
      next: (res) => {
        this.request = res;
      },
      error: (err) => {
        console.error('Failed to load request details', err);
        this.request = null;
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' {
    if (status === 'Approved') return 'success';
    if (status === 'Pending') return 'warning';
    if (status === 'Rejected' || status === 'Cancelled' || status === 'Critical') return 'danger';
    if (status === 'High') return 'primary';
    return 'default';
  }

  approveRequest(): void {
    if (!this.request || !this.requestId) return;
    this.isProcessing = true;
    this.procurementService.approveRequest(this.requestId, this.remarks || 'Approved by Procurement Manager').subscribe({
      next: () => {
        this.isProcessing = false;
        alert('Procurement Request Approved successfully! Now eligible for Vendor Assignment.');
        this.router.navigate([`/procurement/assign-vendor/${this.requestId}`]);
      },
      error: (err) => {
        this.isProcessing = false;
        alert('Failed to approve request: ' + (err.error?.detail || err.message));
      }
    });
  }

  rejectRequest(): void {
    if (!this.request || !this.requestId) return;
    if (!this.remarks.trim()) {
      alert('Please provide remarks explaining why the request is rejected.');
      return;
    }
    this.isProcessing = true;
    this.procurementService.rejectRequest(this.requestId, this.remarks).subscribe({
      next: () => {
        this.isProcessing = false;
        alert('Procurement Request Rejected.');
        this.router.navigate(['/procurement/requests']);
      },
      error: (err) => {
        this.isProcessing = false;
        alert('Failed to reject request: ' + (err.error?.detail || err.message));
      }
    });
  }

  sendBack(): void {
    if (!this.request || !this.requestId) return;
    if (!this.remarks.trim()) {
      alert('Please provide remarks explaining what needs modification.');
      return;
    }
    this.isProcessing = true;
    this.procurementService.sendBackRequest(this.requestId, this.remarks).subscribe({
      next: () => {
        this.isProcessing = false;
        alert('Procurement Request Sent Back for Modification.');
        this.router.navigate(['/procurement/requests']);
      },
      error: (err) => {
        this.isProcessing = false;
        alert('Failed to send back request: ' + (err.error?.detail || err.message));
      }
    });
  }
}
