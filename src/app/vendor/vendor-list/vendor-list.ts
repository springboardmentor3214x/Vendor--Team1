import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

@Component({
  selector: 'app-vendor-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule
  ],
  templateUrl: './vendor-list.html',
  styleUrl: './vendor-list.css'
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

  constructor(private vendorService: VendorService) {}

  ngOnInit(): void {

    this.vendorService.vendors$.subscribe(data => {

      this.vendors = data;

      this.filterVendors();

    });

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

}