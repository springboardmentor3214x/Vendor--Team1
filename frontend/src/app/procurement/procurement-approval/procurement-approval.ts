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
        this.request = {
          id: res.id,
          requestNumber: `PR-${res.id}`,
          title: res.item_name,
          department: 'Procurement',
          requestedBy: 'Procurement Team',
          itemCategory: 'General',
          itemName: res.item_name,
          quantity: res.quantity,
          uom: 'Units',
          budget: res.total_price,
          requiredDate: res.expected_delivery_date,
          priority: 'Medium',
          justification: 'Procurement request',
          status: res.status,
          createdDate: res.expected_delivery_date
        };
      },
      error: () => {
        this.request = null;
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
          this.procurementService.placeOrder(this.requestId!).subscribe({
            next: () => {
              alert('Request approved and purchase order placed.');
              this.router.navigate(['/procurement/requests']);
            },
            error: () => {
              alert('Approved but order placement failed.');
              this.router.navigate(['/procurement/requests']);
            }
          });
        },
        error: () => {
          alert('Could not approve this request.');
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
          error: () => {
            alert('Could not reject this request.');
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
