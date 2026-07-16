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
}

const PLACEHOLDER_VENDOR_LIST_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorList(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_LIST_ROWS;
  }
  return rows.filter((row) => !!row);
}
