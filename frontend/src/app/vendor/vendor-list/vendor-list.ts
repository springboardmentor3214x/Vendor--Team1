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
}

const PLACEHOLDER_VENDOR_LIST_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorList(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_LIST_ROWS;
}
