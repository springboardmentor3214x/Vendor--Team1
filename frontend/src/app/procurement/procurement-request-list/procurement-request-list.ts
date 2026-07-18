import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-procurement-request-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './procurement-request-list.html',
  styleUrls: ['./procurement-request-list.css'],
})
export class ProcurementRequestList implements OnInit {
  rawRequests: any[] = [];
  filteredRequests: any[] = [];
  pagedRequests: any[] = [];
  loading = true;
  errorMsg = '';

  searchQuery = '';
  selectedDepartment = '';
  selectedStatus = '';
  selectedPriority = '';
  sortBy = 'created_at_desc';

  currentPage = 1;
  pageSize = 10;
  totalPages = 1;

  selectedRequestForView: any = null;
  statusHistory: any[] = [];

  userRole: string = '';

  departments = ['IT Department', 'Operations', 'Finance', 'Logistics', 'Administration', 'HR', 'R&D'];
  statuses = ['Draft', 'Pending', 'Approved', 'Vendor Assigned', 'Ordered', 'In Transit', 'Delivered', 'Completed', 'Cancelled', 'Modification Required'];
  priorities = ['Low', 'Medium', 'High', 'Critical'];

  Math = Math;

  constructor(
    private procurementService: ProcurementService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    this.userRole = user?.role || '';
    this.loadRequests();
  }

  loadRequests(): void {
    this.loading = true;
    this.errorMsg = '';
    this.procurementService.getAllProcurementRequests().subscribe({
      next: (res) => {
        this.loading = false;
        if (Array.isArray(res)) {
          this.rawRequests = res;
          this.applyFilters();
        } else {
          this.rawRequests = [];
          this.filteredRequests = [];
          this.pagedRequests = [];
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Error fetching procurement requests', err);
        this.errorMsg = 'Failed to load procurement requests from server.';
      }
    });
  }

  applyFilters(): void {
    let result = [...this.rawRequests];

    if (this.searchQuery.trim()) {
      const q = this.searchQuery.toLowerCase().trim();
      result = result.filter(r => {
        const reqNum = (r.request_number || ('PR-' + r.id)).toLowerCase();
        const formattedPR = ('pr-' + r.id).toLowerCase();
        const reqTitle = (r.request_title || '').toLowerCase();
        const itemName = (r.item_name || '').toLowerCase();
        const requestedBy = (r.requested_by || '').toLowerCase();
        const dept = (r.department || '').toLowerCase();

        return reqNum.includes(q) || formattedPR.includes(q) || reqTitle.includes(q) || itemName.includes(q) || requestedBy.includes(q) || dept.includes(q);
      });
    }

    if (this.selectedDepartment) {
      result = result.filter(r => (r.department || '').toLowerCase() === this.selectedDepartment.toLowerCase());
    }

    if (this.selectedStatus) {
      result = result.filter(r => (r.status || '').toLowerCase() === this.selectedStatus.toLowerCase());
    }

    if (this.selectedPriority) {
      result = result.filter(r => (r.priority || '').toLowerCase() === this.selectedPriority.toLowerCase());
    }

    result.sort((a, b) => {
      if (this.sortBy === 'created_at_desc') {
        return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime();
      } else if (this.sortBy === 'created_at_asc') {
        return new Date(a.created_at || 0).getTime() - new Date(b.created_at || 0).getTime();
      } else if (this.sortBy === 'budget_desc') {
        return (b.total_price || 0) - (a.total_price || 0);
      } else if (this.sortBy === 'budget_asc') {
        return (a.total_price || 0) - (b.total_price || 0);
      }
      return 0;
    });

    this.filteredRequests = result;
    this.currentPage = 1;
    this.updatePagination();
  }

  updatePagination(): void {
    this.totalPages = Math.ceil(this.filteredRequests.length / this.pageSize) || 1;
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    this.pagedRequests = this.filteredRequests.slice(startIndex, endIndex);
  }

  setPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.updatePagination();
    }
  }

  viewDetails(req: any): void {
    this.selectedRequestForView = req;
    this.procurementService.getProcurementStatusHistory(req.id).subscribe({
      next: (history) => this.statusHistory = history,
      error: () => this.statusHistory = []
    });
  }

  closeModal(): void {
    this.selectedRequestForView = null;
    this.statusHistory = [];
  }

  deleteRequest(id: number): void {
    if (confirm(`Are you sure you want to delete Procurement Request #PR-${id}?`)) {
      this.procurementService.deleteProcurementRequest(id).subscribe({
        next: () => {
          alert('Procurement request deleted successfully.');
          this.loadRequests();
        },
        error: (err) => alert('Failed to delete request: ' + (err.error?.detail || err.message))
      });
    }
  }

  createPO(req: any): void {
    this.router.navigate(['/procurement/purchase-order/create'], {
      queryParams: { procurement_id: req.id, vendor_id: req.vendor_id }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' | 'info' {
    switch (status) {
      case 'Approved': return 'success';
      case 'Ordered':
      case 'In Transit': return 'primary';
      case 'Completed':
      case 'Delivered': return 'info';
      case 'Pending':
      case 'Vendor Assigned':
      case 'Modification Required': return 'warning';
      case 'Cancelled':
      case 'Rejected': return 'danger';
      default: return 'default';
    }
  }

  getPriorityBadge(priority: string): 'danger' | 'warning' | 'info' | 'default' {
    switch (priority) {
      case 'Critical': return 'danger';
      case 'High': return 'warning';
      case 'Medium': return 'info';
      default: return 'default';
    }
  }

  canApprove(): boolean {
    return ['Procurement Manager', 'Administrator'].includes(this.userRole);
  }

  canEdit(req: any): boolean {
    return ['Pending', 'Draft', 'Modification Required'].includes(req.status);
  }
}
