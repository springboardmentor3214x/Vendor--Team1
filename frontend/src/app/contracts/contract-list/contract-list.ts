import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-contract-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button, Badge],
  templateUrl: './contract-list.html',
  styleUrls: ['./contract-list.css']
})
export class ContractList implements OnInit {
  allContracts: any[] = [];
  filtered: any[] = [];
  paginated: any[] = [];

  isLoading = true;
  errorMsg = '';
  actionMsg = '';

  searchText = '';
  statusFilter = 'All';
  expiryFilter = 'All';

  sortColumn: 'contract_number' | 'vendor_name' | 'contract_value' | 'end_date' = 'end_date';
  sortAscending = true;

  currentPage = 1;
  itemsPerPage = 8;
  totalPages = 1;

  totalContracts = 0;
  activeContracts = 0;
  expiringContracts = 0;
  expiredContracts = 0;
  totalValue = 0;

  role = '';

  constructor(
    private contractService: ContractService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.role = this.authService.getUserRole() || '';
    this.loadContracts();
  }

  get canDelete(): boolean {
    return this.role === 'Administrator';
  }

  get canEdit(): boolean {
    return this.role === 'Administrator' || this.role === 'Procurement Manager';
  }

  loadContracts(): void {
    this.isLoading = true;
    this.errorMsg = '';
    this.contractService.getContracts().subscribe({
      next: (res) => {
        this.isLoading = false;
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        this.allContracts = (res || []).map(c => {
          const end = c.end_date ? new Date(c.end_date) : null;
          const daysToExpiry = end
            ? Math.ceil((end.getTime() - today.getTime()) / 86400000)
            : null;
          return { ...c, daysToExpiry };
        });

        this.computeSummary();
        this.applyFilters();
      },
      error: () => {
        this.isLoading = false;
        this.errorMsg = 'Could not load contracts. Please try again.';
      }
    });
  }

  private computeSummary(): void {
    this.totalContracts = this.allContracts.length;
    this.activeContracts = this.allContracts.filter(c => c.status === 'Active').length;

    this.expiringContracts = this.allContracts.filter(
      c => c.daysToExpiry !== null && c.daysToExpiry >= 0 && c.daysToExpiry <= 90
    ).length;
    this.expiredContracts = this.allContracts.filter(
      c => c.daysToExpiry !== null && c.daysToExpiry < 0
    ).length;
    this.totalValue = this.allContracts.reduce((sum, c) => sum + (c.contract_value || 0), 0);
  }

  applyFilters(): void {
    const term = this.searchText.toLowerCase().trim();

    this.filtered = this.allContracts.filter(c => {
      const matchesSearch = !term ||
        (c.contract_number || '').toLowerCase().includes(term) ||
        (c.contract_title || '').toLowerCase().includes(term) ||
        (c.vendor_name || '').toLowerCase().includes(term) ||
        (c.responsible_manager || '').toLowerCase().includes(term) ||
        (c.procurement_category || '').toLowerCase().includes(term);

      const matchesStatus = this.statusFilter === 'All' || c.status === this.statusFilter;

      let matchesExpiry = true;
      if (this.expiryFilter === 'Expired') {
        matchesExpiry = c.daysToExpiry !== null && c.daysToExpiry < 0;
      } else if (this.expiryFilter !== 'All') {
        const window = Number(this.expiryFilter);
        matchesExpiry = c.daysToExpiry !== null && c.daysToExpiry >= 0 && c.daysToExpiry <= window;
      }

      return matchesSearch && matchesStatus && matchesExpiry;
    });

    this.sortData(false);
  }

  sortBy(column: 'contract_number' | 'vendor_name' | 'contract_value' | 'end_date'): void {
    if (this.sortColumn === column) {
      this.sortAscending = !this.sortAscending;
    } else {
      this.sortColumn = column;
      this.sortAscending = true;
    }
    this.sortData(false);
  }

  private sortData(resetToggle: boolean): void {
    this.filtered.sort((a, b) => {
      const left = a[this.sortColumn];
      const right = b[this.sortColumn];
      if (this.sortColumn === 'contract_value') {
        return this.sortAscending ? (left || 0) - (right || 0) : (right || 0) - (left || 0);
      }
      const l = String(left || '');
      const r = String(right || '');
      return this.sortAscending ? l.localeCompare(r) : r.localeCompare(l);
    });
    this.currentPage = 1;
    this.updatePagination();
  }

  updatePagination(): void {
    this.totalPages = Math.max(1, Math.ceil(this.filtered.length / this.itemsPerPage));
    if (this.currentPage > this.totalPages) this.currentPage = this.totalPages;
    const start = (this.currentPage - 1) * this.itemsPerPage;
    this.paginated = this.filtered.slice(start, start + this.itemsPerPage);
  }

  previousPage(): void {
    if (this.currentPage > 1) { this.currentPage--; this.updatePagination(); }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) { this.currentPage++; this.updatePagination(); }
  }

  effectiveStatus(c: any): string {
    if (c.daysToExpiry !== null && c.daysToExpiry < 0) return 'Expired';
    if (c.daysToExpiry !== null && c.daysToExpiry <= 30 && c.status === 'Active') return 'Expiring Soon';
    return c.status;
  }

  statusVariant(status: string): 'success' | 'warning' | 'danger' | 'default' {
    if (status === 'Active') return 'success';
    if (status === 'Expiring Soon' || status === 'Draft') return 'warning';
    if (status === 'Expired' || status === 'Terminated') return 'danger';
    return 'default';
  }

  renewContract(c: any): void {
    const suggested = new Date();
    suggested.setFullYear(suggested.getFullYear() + 1);
    const input = prompt(
      `Renew ${c.contract_number || 'contract'} — enter the new end date (YYYY-MM-DD):`,
      suggested.toISOString().slice(0, 10)
    );
    if (!input) return;

    this.actionMsg = '';
    this.errorMsg = '';
    this.contractService.renewContract(c.id, input).subscribe({
      next: () => {
        this.actionMsg = `Contract ${c.contract_number} renewed to ${input}.`;
        this.loadContracts();
      },
      error: (err) => this.errorMsg = err.error?.detail || 'Could not renew the contract.'
    });
  }

  deleteContract(c: any): void {
    if (!confirm(`Delete contract ${c.contract_number || c.id}? This cannot be undone.`)) return;

    this.actionMsg = '';
    this.errorMsg = '';
    this.contractService.deleteContract(c.id).subscribe({
      next: () => {
        this.actionMsg = 'Contract deleted.';
        this.loadContracts();
      },
      error: (err) => this.errorMsg = err.error?.detail || 'Could not delete the contract.'
    });
  }
}
