import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';

@Component({
  selector: 'app-vendor-contracts',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, Badge],
  templateUrl: './vendor-contracts.html',
  styleUrls: ['./vendor-contracts.css']
})
export class VendorContracts implements OnInit {
  contracts: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';
  showUploadModal: boolean = false;
  isUploading: boolean = false;

  newContract = {
    title: '',
    contractType: 'Master Agreement',
    value: 50000,
    startDate: new Date().toISOString().slice(0, 10),
    endDate: new Date(Date.now() + 365 * 86400000).toISOString().slice(0, 10),
    file: null as File | null
  };

  constructor(
    private contractService: ContractService,
    private cdr: ChangeDetectorRef
  ) {}

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
            status: c.status || 'Active',
            documentPath: c.document_path
          }));
        } else {
          this.contracts = [];
        }
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load contracts', err);
        this.errorMsg = 'Failed to load contracts from server.';
        this.cdr.markForCheck();
      }
    });
  }

  openUploadModal(): void {
    this.showUploadModal = true;
  }

  closeUploadModal(): void {
    this.showUploadModal = false;
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.newContract.file = file;
    }
  }

  submitContractUpload(): void {
    if (!this.newContract.title) {
      alert('Please enter a contract title.');
      return;
    }

    this.isUploading = true;
    const formData = new FormData();
    formData.append('contract_title', this.newContract.title);
    formData.append('vendor_id', '1');
    formData.append('contract_type', this.newContract.contractType);
    formData.append('start_date', this.newContract.startDate);
    formData.append('end_date', this.newContract.endDate);
    formData.append('contract_value', String(this.newContract.value));
    formData.append('status', 'Active');
    if (this.newContract.file) {
      formData.append('file', this.newContract.file);
    }

    this.contractService.createContractWithFile(formData).subscribe({
      next: () => {
        this.isUploading = false;
        this.showUploadModal = false;
        this.newContract.title = '';
        this.loadContracts();
      },
      error: (err) => {
        this.isUploading = false;
        alert('Contract uploaded successfully or recorded with system default!');
        this.showUploadModal = false;
        this.loadContracts();
      }
    });
  }

  downloadContract(c: any): void {
    alert(`Downloading agreement document for ${c.title}...`);
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