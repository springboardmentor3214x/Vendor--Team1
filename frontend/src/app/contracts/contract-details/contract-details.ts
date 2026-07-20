import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';

@Component({
  selector: 'app-contract-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Badge],
  templateUrl: './contract-details.html',
  styleUrls: ['./contract-details.css']
})
export class ContractDetails implements OnInit {
  contract: any = null;
  certifications: any[] = [];
  compliance: any[] = [];

  loading = true;
  errorMsg = '';
  daysToExpiry: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private contractService: ContractService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.contractService.getContractById(id).subscribe({
      next: (c) => {
        this.loading = false;
        this.contract = c;

        if (c.end_date) {
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          this.daysToExpiry = Math.ceil((new Date(c.end_date).getTime() - today.getTime()) / 86400000);
        }

        if (c.vendor_id) {
          this.contractService.getVendorCertifications(c.vendor_id).subscribe({
            next: (res) => this.certifications = res || [],
            error: () => this.certifications = []
          });
          this.contractService.getVendorCompliance(c.vendor_id).subscribe({
            next: (res) => this.compliance = res || [],
            error: () => this.compliance = []
          });
        }
      },
      error: () => {
        this.loading = false;
        this.errorMsg = 'Could not load the contract.';
      }
    });
  }

  get effectiveStatus(): string {
    if (this.daysToExpiry !== null && this.daysToExpiry < 0) return 'Expired';
    if (this.daysToExpiry !== null && this.daysToExpiry <= 30 && this.contract?.status === 'Active') return 'Expiring Soon';
    return this.contract?.status || '-';
  }

  statusVariant(status: string): 'success' | 'warning' | 'danger' | 'default' {
    if (status === 'Active' || status === 'Compliant') return 'success';
    if (status === 'Expiring Soon' || status === 'Draft' || status === 'Pending Verification') return 'warning';
    if (status === 'Expired' || status === 'Terminated' || status === 'Non-Compliant') return 'danger';
    return 'default';
  }

  downloadDocument(): void {
    if (!this.contract?.id) {
      return;
    }

    this.contractService.downloadContractDocument(this.contract.id).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        window.open(url, '_blank');
        setTimeout(() => URL.revokeObjectURL(url), 60000);
      },
      error: (err) => {
        this.errorMsg = err.error?.detail || 'The agreement document could not be opened.';
      }
    });
  }

  edit(): void {
    this.router.navigate(['/contract-management/edit', this.contract.id]);
  }
}
