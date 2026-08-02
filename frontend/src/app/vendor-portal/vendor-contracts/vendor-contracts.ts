import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';

@Component({
  selector: 'app-vendor-contracts',
  standalone: true,
  imports: [CommonModule, Card, Button, Badge],
  templateUrl: './vendor-contracts.html',
  styleUrls: ['./vendor-contracts.css']
})
export class VendorContracts implements OnInit {
  contracts: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';

  constructor(private contractService: ContractService) {}

  ngOnInit(): void {
    this.loadContracts();
  }

  loadContracts(): void {
    this.loading = true;
    this.errorMsg = '';
    this.contractService.getContracts().subscribe({
      next: (data) => {
        this.loading = false;
        if (Array.isArray(data)) {
          this.contracts = data.map(c => ({
            id: c.id,
            title: c.contract_title || c.title || 'Service Agreement',
            vendorName: c.vendor_name || 'Vendor',
            startDate: c.start_date ? c.start_date.slice(0, 10) : '2026-01-01',
            endDate: c.end_date ? c.end_date.slice(0, 10) : '2027-01-01',
            value: c.contract_value || c.value || 0,
            status: c.status || 'Active'
          }));
        } else {
          this.contracts = [];
        }
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load contracts', err);
        this.errorMsg = 'Failed to load contracts from server.';
      }
    });
  }

  upload(): void {
    const title = prompt('Enter Contract Title:');
    if (!title) return;
    this.contractService.createContract({
      contract_title: title,
      vendor_id: 1,
      start_date: new Date().toISOString(),
      end_date: new Date(Date.now() + 365 * 86400000).toISOString(),
      contract_value: 50000.00,
      status: 'Active'
    }).subscribe({
      next: () => this.loadContracts(),
      error: (err) => alert('Failed to create contract: ' + (err.error?.detail || err.message))
    });
  }

  getBadgeVariant(status: string): 'primary' | 'danger' | 'success' | 'warning' | 'default' | 'info' {
    switch (status) {
      case 'Active': return 'success';
      case 'Pending': return 'warning';
      case 'Expired':
      case 'Terminated': return 'danger';
      default: return 'default';
    }
  }
}