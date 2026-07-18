import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

export interface StatusHistoryMock {
  status: string;
  updatedBy: string;
  updatedAt: string;
  remarks: string;
}

@Component({
  selector: 'app-procurement-status',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './procurement-status.html',
  styleUrls: ['./procurement-status.css'],
})
export class ProcurementStatus implements OnInit {
  poId: string | null = null;
  currentStatus: string = 'Ordered';
  
  stages = ['Pending', 'Approved', 'Ordered', 'Delivered', 'Completed'];

  history: StatusHistoryMock[] = [
    { status: 'Ordered', updatedBy: 'Procurement Manager', updatedAt: '16 Jul 2026, 10:30 AM', remarks: 'PO generated and sent to vendor.' },
    { status: 'Approved', updatedBy: 'Admin User', updatedAt: '15 Jul 2026, 02:15 PM', remarks: 'Request approved for Vendor Assignment.' },
    { status: 'Pending', updatedBy: 'Alice Smith', updatedAt: '15 Jul 2026, 09:00 AM', remarks: 'Procurement Request Created.' }
  ];

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.poId = this.route.snapshot.paramMap.get('id');
  }

  isStageCompleted(stage: string): boolean {
    const currentIndex = this.stages.indexOf(this.currentStatus);
    const stageIndex = this.stages.indexOf(stage);
    return stageIndex <= currentIndex;
  }

  updateStatus(newStatus: string): void {
    if (confirm(`Update status to ${newStatus}?`)) {
      this.currentStatus = newStatus;
      this.history.unshift({
        status: newStatus,
        updatedBy: 'Current User',
        updatedAt: new Date().toLocaleString(),
        remarks: `Manually updated status to ${newStatus}`
      });
      alert('Status updated successfully.');
    }
  }

  cancelProcurement(): void {
    if (confirm('Are you sure you want to cancel this procurement? This cannot be undone.')) {
      this.currentStatus = 'Cancelled';
      this.history.unshift({
        status: 'Cancelled',
        updatedBy: 'Current User',
        updatedAt: new Date().toLocaleString(),
        remarks: 'Procurement was cancelled.'
      });
    }
  }
}
