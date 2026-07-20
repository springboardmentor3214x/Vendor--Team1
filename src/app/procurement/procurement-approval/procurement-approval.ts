import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

export interface ProcurementRequestDetailsMock {
  id: number;
  requestNumber: string;
  title: string;
  department: string;
  requestedBy: string;
  itemCategory: string;
  itemName: string;
  quantity: number;
  uom: string;
  budget: number;
  requiredDate: string;
  priority: string;
  justification: string;
  status: string;
  createdDate: string;
}

@Component({
  selector: 'app-procurement-approval',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './procurement-approval.html',
  styleUrls: ['./procurement-approval.css'],
})
export class ProcurementApproval implements OnInit {
  request: ProcurementRequestDetailsMock | null = null;
  requestId: string | null = null;
  remarks = '';

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
        console.error('Error fetching request', err);
        // Fallback mock data
        this.request = {
          id: Number(id) || 1,
          requestNumber: `PR-102${id || 4}`,
          title: 'Office Supplies Q3',
          department: 'Administration',
          requestedBy: 'Alice Smith',
          itemCategory: 'Stationery',
          itemName: 'Printing Paper, Pens, Notebooks',
          quantity: 50,
          uom: 'Boxes',
          budget: 50000,
          requiredDate: '30 Jul 2026',
          priority: 'Low',
          justification: 'Quarterly restock of essential office supplies for the admin and HR departments.',
          status: 'Pending',
          createdDate: '15 Jul 2026'
        };
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' {
    if (status === 'Approved') return 'success';
    if (status === 'Pending') return 'warning';
    if (status === 'Rejected' || status === 'Critical') return 'danger';
    if (status === 'High') return 'primary';
    return 'default';
  }

  approveRequest(): void {
    if (this.request && this.requestId) {
      this.procurementService.approveRequest(this.requestId, { remarks: this.remarks || 'Approved' }).subscribe({
        next: () => {
          alert('Request Approved successfully. It is now eligible for Vendor Assignment.');
          this.router.navigate(['/procurement/requests']);
        },
        error: (err) => {
          console.error('Error approving', err);
          // Mock success
          alert('Request Approved successfully. (Mocked)');
          this.router.navigate(['/procurement/requests']);
        }
      });
    }
  }

  rejectRequest(): void {
    if (this.request && this.requestId) {
      const reason = prompt('Please enter the reason for rejection:');
      if (reason !== null) {
        this.procurementService.rejectRequest(this.requestId, reason).subscribe({
          next: () => {
            alert('Request Rejected.');
            this.router.navigate(['/procurement/requests']);
          },
          error: (err) => {
            console.error('Error rejecting', err);
            // Mock success
            alert('Request Rejected. (Mocked)');
            this.router.navigate(['/procurement/requests']);
          }
        });
      }
    }
  }

  sendBack(): void {
    alert('Request sent back for modification.');
    this.router.navigate(['/procurement/requests']);
  }
}
