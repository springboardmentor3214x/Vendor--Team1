import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-procurement-status',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './procurement-status.html',
  styleUrls: ['./procurement-status.css'],
})
export class ProcurementStatus implements OnInit {
  procurementId: string | null = null;
  procurement: any = null;
  currentStatus: string = 'Pending';
  newRemarks: string = '';
  isLoading = true;

  stages = ['Pending', 'Approved', 'Ordered', 'Delivered', 'Completed'];

  history: any[] = [];
  userRole: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private procurementService: ProcurementService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    this.userRole = user?.role || '';
    this.procurementId = this.route.snapshot.paramMap.get('id');
    if (this.procurementId) {
      this.loadProcurementData(this.procurementId);
    }
  }

  loadProcurementData(id: string): void {
    this.isLoading = true;
    this.procurementService.getProcurementRequestById(id).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.procurement = res;
        this.currentStatus = res.status || 'Pending';
        this.loadHistory(id);
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error fetching procurement status', err);
      }
    });
  }

  loadHistory(id: string): void {
    this.procurementService.getProcurementStatusHistory(id).subscribe({
      next: (res) => this.history = res,
      error: () => this.history = []
    });
  }

  isStageCompleted(stage: string): boolean {
    if (this.currentStatus === 'Cancelled') return false;
    const currentIndex = this.stages.indexOf(this.currentStatus);
    const stageIndex = this.stages.indexOf(stage);
    return stageIndex <= currentIndex && currentIndex !== -1;
  }

  updateStatus(targetStage: string): void {
    if (!this.procurementId) return;

    if (targetStage === 'Delivered') {
      this.procurementService.deliverRequest(this.procurementId).subscribe({
        next: () => {
          alert('Procurement status updated to Delivered!');
          this.loadProcurementData(this.procurementId!);
        },
        error: (err: any) => alert('Failed to update status: ' + (err.error?.detail || err.message))
      });
    } else if (targetStage === 'Completed') {
      this.procurementService.completeRequest(this.procurementId).subscribe({
        next: () => {
          alert('Procurement completed successfully!');
          this.loadProcurementData(this.procurementId!);
        },
        error: (err: any) => alert('Failed to update status: ' + (err.error?.detail || err.message))
      });
    }
  }

  cancelProcurement(): void {
    if (!this.procurementId) return;
    const reason = prompt('Please enter cancellation reason:');
    if (reason !== null) {
      this.procurementService.rejectRequest(this.procurementId, reason || 'Cancelled by user').subscribe({
        next: () => {
          alert('Procurement cancelled.');
          this.loadProcurementData(this.procurementId!);
        },
        error: (err: any) => alert('Failed to cancel: ' + (err.error?.detail || err.message))
      });
    }
  }
}
