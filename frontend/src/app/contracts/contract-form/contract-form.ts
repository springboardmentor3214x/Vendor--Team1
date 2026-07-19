import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { ContractService } from '../../core/services/contract.service';
import { VendorService } from '../../services/vendor';

@Component({
  selector: 'app-contract-form',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button],
  templateUrl: './contract-form.html',
  styleUrls: ['./contract-form.css']
})
export class ContractForm implements OnInit {
  isEdit = false;
  contractId: number | null = null;

  contract: any = {
    contract_title: '',
    vendor_id: null,
    contract_type: 'Master Agreement',
    procurement_category: '',
    start_date: '',
    end_date: '',
    contract_value: null,
    payment_terms: 'Net 30',
    sla_details: '',
    warranty_details: '',
    responsible_manager: '',
    status: 'Draft'
  };

  vendors: any[] = [];
  documentFile: File | null = null;

  loading = true;
  saving = false;
  errorMsg = '';
  fileError = '';

  contractTypes = ['Master Agreement', 'Rate Contract', 'Service Level Agreement', 'Supply Agreement', 'NDA'];
  paymentTermOptions = ['Net 15', 'Net 30', 'Net 45', 'Net 60', 'Advance', 'Milestone Based'];
  categories = ['IT Equipment', 'Software Licenses', 'Cloud Services', 'Raw Materials',
                'Office Supplies', 'Furniture', 'Packaging', 'Logistics', 'Safety', 'Consumables'];
  statuses = ['Draft', 'Active', 'Expiring Soon', 'Expired', 'Renewed', 'Terminated'];

  readonly allowedExtensions = ['pdf', 'jpg', 'jpeg', 'png'];
  readonly maxFileSizeBytes = 10 * 1024 * 1024;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private contractService: ContractService,
    private vendorService: VendorService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.isEdit = !!id;
    this.contractId = id ? Number(id) : null;

    this.vendorService.loadVendors().subscribe({
      next: (vendors) => {
        this.vendors = (vendors || []).filter(
          v => v.approvalStatus === 'Approved' && v.status === 'Active'
        );
        if (!this.isEdit) this.loading = false;
      },
      error: () => {
        this.vendors = [];
        this.loading = false;
        this.errorMsg = 'Could not load vendors.';
      }
    });

    if (this.contractId) {
      this.contractService.getContractById(this.contractId).subscribe({
        next: (c) => {
          this.loading = false;
          this.contract = {
            ...c,
            start_date: (c.start_date || '').slice(0, 10),
            end_date: (c.end_date || '').slice(0, 10)
          };
        },
        error: () => {
          this.loading = false;
          this.errorMsg = 'Could not load the contract.';
        }
      });
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.fileError = '';
    if (!input.files || input.files.length === 0) {
      this.documentFile = null;
      return;
    }
    const file = input.files[0];
    const ext = (file.name.split('.').pop() || '').toLowerCase();

    if (!this.allowedExtensions.includes(ext)) {
      this.fileError = `"${file.name}" is not supported. Upload a PDF, JPG or PNG.`;
      input.value = '';
      this.documentFile = null;
      return;
    }
    if (file.size > this.maxFileSizeBytes) {
      this.fileError = `"${file.name}" is ${(file.size / (1024 * 1024)).toFixed(1)} MB. Maximum is 10 MB.`;
      input.value = '';
      this.documentFile = null;
      return;
    }
    this.documentFile = file;
  }

  private validate(): string {
    const c = this.contract;
    if (!c.contract_title?.trim()) return 'Contract title is required.';
    if (!c.vendor_id) return 'Select a vendor.';
    if (!c.start_date) return 'Start date is required.';
    if (!c.end_date) return 'End date is required.';
    if (new Date(c.end_date) <= new Date(c.start_date)) return 'End date must be after the start date.';
    if (c.contract_value === null || c.contract_value === '' || isNaN(Number(c.contract_value))) {
      return 'Contract value must be a number.';
    }
    if (Number(c.contract_value) <= 0) return 'Contract value must be greater than zero.';
    return '';
  }

  save(): void {
    this.errorMsg = '';
    const problem = this.validate();
    if (problem) { this.errorMsg = problem; return; }

    const vendor = this.vendors.find(v => v.id === Number(this.contract.vendor_id));
    const payload = {
      ...this.contract,
      vendor_id: Number(this.contract.vendor_id),
      vendor_name: vendor?.companyName || this.contract.vendor_name,
      contract_value: Number(this.contract.contract_value)
    };

    this.saving = true;

    if (this.isEdit && this.contractId) {
      this.contractService.updateContract(this.contractId, payload).subscribe({
        next: () => this.router.navigate(['/contract-management']),
        error: (err) => {
          this.saving = false;
          this.errorMsg = err.error?.detail || 'Could not update the contract.';
        }
      });
      return;
    }

    if (this.documentFile) {
      const form = new FormData();
      Object.entries(payload).forEach(([k, v]) => {
        if (v !== null && v !== undefined && v !== '') form.append(k, String(v));
      });
      form.append('file', this.documentFile);

      this.contractService.createContractWithFile(form).subscribe({
        next: () => this.router.navigate(['/contract-management']),
        error: (err) => {
          this.saving = false;
          this.errorMsg = err.error?.detail || 'Could not create the contract.';
        }
      });
    } else {
      this.contractService.createContract(payload).subscribe({
        next: () => this.router.navigate(['/contract-management']),
        error: (err) => {
          this.saving = false;
          this.errorMsg = err.error?.detail || 'Could not create the contract.';
        }
      });
    }
  }

  cancel(): void {
    this.router.navigate(['/contract-management']);
  }
}
