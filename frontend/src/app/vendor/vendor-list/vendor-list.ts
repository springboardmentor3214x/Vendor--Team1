import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

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

  searchText = '';

  selectedCategory = 'All';

  selectedStatus = 'All';

  sortAscending = true;

  currentPage = 1;

  itemsPerPage = 5;

  totalPages = 1;

  totalVendors = 0;

  activeVendors = 0;

  pendingVendors = 0;

  suspendedVendors = 0;

  rejectedVendors = 0;

  constructor(private vendorService: VendorService) {}

  ngOnInit(): void {

    this.vendorService.vendors$.subscribe(data => {

      this.vendors = data;

      this.updateStatistics();

      this.filterVendors();

    });

  }

  updateStatistics(): void {

    this.totalVendors = this.vendors.length;

    this.activeVendors = this.vendors.filter(
      vendor => vendor.status === 'Active'
    ).length;

    this.pendingVendors = this.vendors.filter(
      vendor => vendor.status === 'Pending'
    ).length;

    this.suspendedVendors = this.vendors.filter(
      vendor => vendor.status === 'Suspended'
    ).length;

    this.rejectedVendors = this.vendors.filter(
      vendor => vendor.status === 'Rejected'
    ).length;

  }

  filterVendors(): void {

    const search = this.searchText.toLowerCase().trim();

    this.filteredVendors = this.vendors.filter(vendor => {

      const matchesSearch =

        vendor.companyName.toLowerCase().includes(search) ||

        vendor.contactPerson.toLowerCase().includes(search) ||

        vendor.category.toLowerCase().includes(search);

      const matchesCategory =

        this.selectedCategory === 'All' ||

        vendor.category === this.selectedCategory;

      const matchesStatus =

        this.selectedStatus === 'All' ||

        vendor.status === this.selectedStatus;

      return matchesSearch && matchesCategory && matchesStatus;

    });

    this.sortData(false);

  }

  sortData(toggle: boolean = true): void {

    if (toggle) {

      this.sortAscending = !this.sortAscending;

    }

    this.filteredVendors.sort((a, b) => {

      return this.sortAscending

        ? a.companyName.localeCompare(b.companyName)

        : b.companyName.localeCompare(a.companyName);

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

  deleteVendor(id: number): void {

    const confirmed = confirm(
      'Are you sure you want to delete this vendor?'
    );

    if (!confirmed) {

      return;

    }

    this.vendorService.deleteVendor(id);

  }

  approveVendor(id: number): void {

    this.vendorService.approveVendor(id);

  }

  rejectVendor(id: number): void {

    this.vendorService.rejectVendor(id);

  }

  activateVendor(id: number): void {

    this.vendorService.activateVendor(id);

  }

  suspendVendor(id: number): void {

    this.vendorService.suspendVendor(id);

  }

}