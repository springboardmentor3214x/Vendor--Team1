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
}

const PLACEHOLDER_CONTRACT_LIST_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderContractList(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_CONTRACT_LIST_ROWS;
  }
  return rows.filter((row) => !!row);
}
