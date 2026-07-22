import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';
import { VENDOR_CATEGORIES } from '../../core/vendor-categories';

import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Card } from '../../ui/card/card';

@Component({
  selector: 'app-vendor-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Badge,
    Button,
    InputComponent,
    Card
  ],
  templateUrl: './vendor-list.html',
  styleUrls: ['./vendor-list.css']
})
export class VendorList implements OnInit {

  vendors: Vendor[] = [];
  filteredVendors: Vendor[] = [];
  paginatedVendors: Vendor[] = [];

  readonly categories = VENDOR_CATEGORIES;

  readonly SUSPENDED_STATUSES = ['Suspended', 'Inactive', 'Blocked'];
  readonly SUSPENDED_GROUP = 'Suspended/Inactive';

  searchText = '';
  selectedCategory = 'All';
  selectedStatus = 'All';
  selectedApprovalStatus = 'All';
  sortAscending = true;

  currentPage = 1;
  itemsPerPage = 5;
  totalPages = 1;

  totalVendors = 0;
  approvedVendors = 0;
  activeVendors = 0;
  pendingVendors = 0;
  suspendedVendors = 0;
  rejectedVendors = 0;

  loading = true;
  errorMsg = '';
  actionMsg = '';

  constructor(
    private vendorService: VendorService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.vendorService.vendors$.subscribe(data => {
      this.vendors = data;
      this.updateStatistics();
      this.filterVendors();
      this.cdr.markForCheck();
    });

    this.loadVendors();
  }

  loadVendors(): void {
    this.loading = true;
    this.errorMsg = '';
    this.vendorService.loadVendors().subscribe({
      next: () => {
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: (error) => {
        this.loading = false;
        this.errorMsg = error.error?.detail || 'Could not load vendors. Check that the API is running and sign in again.';
        this.cdr.markForCheck();
      }
    });
  }

  updateStatistics(): void {

    this.totalVendors = this.vendors.length;
    this.approvedVendors = this.vendors.filter(vendor => vendor.approvalStatus === 'Approved').length;
    this.pendingVendors = this.vendors.filter(vendor => vendor.approvalStatus === 'Pending').length;
    this.rejectedVendors = this.vendors.filter(vendor => vendor.approvalStatus === 'Rejected').length;
    this.activeVendors = this.vendors.filter(vendor => vendor.status === 'Active').length;
    this.suspendedVendors = this.vendors.filter(
      vendor => this.SUSPENDED_STATUSES.includes(vendor.status)
    ).length;
  }

  filterByCard(card: 'total' | 'approved' | 'pending' | 'active' | 'suspended' | 'rejected'): void {
    this.searchText = '';
    this.selectedCategory = 'All';
    this.selectedStatus = 'All';
    this.selectedApprovalStatus = 'All';

    switch (card) {
      case 'approved':
        this.selectedApprovalStatus = 'Approved';
        break;
      case 'pending':
        this.selectedApprovalStatus = 'Pending';
        break;
      case 'rejected':
        this.selectedApprovalStatus = 'Rejected';
        break;
      case 'active':
        this.selectedStatus = 'Active';
        break;
      case 'suspended':

        this.selectedStatus = this.SUSPENDED_GROUP;
        break;
    }

    this.filterVendors();
    this.activeCard = card;
  }

  activeCard: string = 'total';

  onFilterChange(): void {
    this.activeCard = '';
    this.filterVendors();
  }

  filterVendors(): void {
    const search = this.searchText.toLowerCase().trim();
    this.filteredVendors = this.vendors.filter(vendor => {

      const matchesSearch = !search ||
        String(vendor.id).includes(search) ||
        (vendor.companyName || '').toLowerCase().includes(search) ||
        (vendor.contactPerson || '').toLowerCase().includes(search) ||
        (vendor.email || '').toLowerCase().includes(search) ||
        (vendor.gst || '').toLowerCase().includes(search) ||
        (vendor.category || '').toLowerCase().includes(search);

      const matchesCategory =
        this.selectedCategory === 'All' ||
        vendor.category === this.selectedCategory;

      const matchesStatus =
        this.selectedStatus === 'All' ||
        (this.selectedStatus === this.SUSPENDED_GROUP
          ? this.SUSPENDED_STATUSES.includes(vendor.status)
          : vendor.status === this.selectedStatus);

      const matchesApproval =
        this.selectedApprovalStatus === 'All' ||
        vendor.approvalStatus === this.selectedApprovalStatus;

      return matchesSearch && matchesCategory && matchesStatus && matchesApproval;
    });

    this.sortData(false);
  }

  sortColumn: 'id' | 'companyName' | 'category' | 'status' | 'approvalStatus' = 'id';

  sortBy(column: 'id' | 'companyName' | 'category' | 'status' | 'approvalStatus'): void {
    if (this.sortColumn === column) {
      this.sortAscending = !this.sortAscending;
    } else {
      this.sortColumn = column;
      this.sortAscending = true;
    }
    this.sortData(false);
  }

  sortData(toggle: boolean = true): void {
    if (toggle) {
      this.sortAscending = !this.sortAscending;
    }

    this.filteredVendors.sort((a, b) => {
      if (this.sortColumn === 'id') {
        return this.sortAscending ? a.id - b.id : b.id - a.id;
      }
      const left = String(a[this.sortColumn] || '');
      const right = String(b[this.sortColumn] || '');
      return this.sortAscending ? left.localeCompare(right) : right.localeCompare(left);
    });

    this.currentPage = 1;
    this.updatePagination();
  }

  updatePagination(): void {
    this.totalPages = Math.ceil(this.filteredVendors.length / this.itemsPerPage);
    if (this.totalPages === 0) {
      this.totalPages = 1;
    }
    if (this.currentPage > this.totalPages) {
      this.currentPage = this.totalPages;
    }

    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    this.paginatedVendors = this.filteredVendors.slice(start, end);
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updatePagination();
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updatePagination();
    }
  }

  private runAction(action: Observable<any>, successMessage: string): void {
    this.errorMsg = '';
    this.actionMsg = '';
    action.subscribe({
      next: () => {
        this.actionMsg = successMessage;
        this.cdr.markForCheck();
      },
      error: (error) => {
        this.errorMsg = error.error?.detail || 'The action could not be completed.';
        this.cdr.markForCheck();
      }
    });
  }

  deleteVendor(id: number): void {
    const confirmed = confirm('Are you sure you want to delete this vendor?');
    if (!confirmed) {
      return;
    }
    this.runAction(this.vendorService.deleteVendor(id), 'Vendor deleted successfully.');
  }

  approveVendor(id: number): void {
    this.runAction(this.vendorService.approveVendor(id), 'Vendor approved successfully.');
  }

  rejectVendor(id: number): void {
    this.runAction(this.vendorService.rejectVendor(id), 'Vendor rejected.');
  }

  activateVendor(id: number): void {
    this.runAction(this.vendorService.activateVendor(id), 'Vendor activated.');
  }

  suspendVendor(id: number): void {
    this.runAction(this.vendorService.suspendVendor(id), 'Vendor suspended.');
  }

}
