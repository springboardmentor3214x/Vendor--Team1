import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';
import { VendorService } from '../../services/vendor';

@Component({
  selector: 'app-compliance-management',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button, Badge],
  templateUrl: './compliance-management.html',
  styleUrls: ['./compliance-management.css']
})
export class ComplianceManagement implements OnInit {
  vendors: any[] = [];
  selectedVendorId: number | null = null;

  certifications: any[] = [];
  complianceRecords: any[] = [];

  loadingVendors = true;
  loadingRecords = false;
  errorMsg = '';
  actionMsg = '';

  showCertForm = false;
  newCert: any = {
    certification_name: '',
    certificate_number: '',
    issuing_authority: '',
    issue_date: '',
    expiry_date: ''
  };

  showComplianceForm = false;
  newCompliance: any = {
    compliance_type: 'GST Compliance',
    status: 'Pending Verification',
    expiry_date: '',
    remarks: ''
  };

  certificationTypes = ['ISO 9001:2015', 'ISO 27001:2022', 'GST Registration', 'Business License',
                        'Manufacturing License', 'Environmental Clearance', 'Cyber Security Audit Clearance'];
  complianceTypes = ['GST Compliance', 'Tax Compliance', 'ISO Compliance', 'Environmental Compliance',
                     'Cybersecurity Standards', 'Labor Law Compliance'];
  complianceStatuses = ['Compliant', 'Pending Verification', 'Non-Compliant', 'Expired'];

  constructor(
    private contractService: ContractService,
    private vendorService: VendorService
  ) {}

  ngOnInit(): void {
    this.vendorService.loadVendors().subscribe({
      next: (vendors) => {
        this.loadingVendors = false;
        this.vendors = (vendors || []).filter(v => v.approvalStatus === 'Approved');
        if (this.vendors.length > 0) {
          this.selectedVendorId = this.vendors[0].id;
          this.loadRecords();
        }
      },
      error: () => {
        this.loadingVendors = false;
        this.errorMsg = 'Could not load vendors.';
      }
    });
  }

  get selectedVendorName(): string {
    return this.vendors.find(v => v.id === Number(this.selectedVendorId))?.companyName || '';
  }

  loadRecords(): void {
    if (!this.selectedVendorId) return;
    this.loadingRecords = true;
    this.errorMsg = '';

    this.contractService.getVendorCertifications(this.selectedVendorId).subscribe({
      next: (res) => {
        this.loadingRecords = false;
        this.certifications = (res || []).map(c => ({ ...c, daysToExpiry: this.daysUntil(c.expiry_date) }));
      },
      error: () => {
        this.loadingRecords = false;
        this.certifications = [];
      }
    });

    this.contractService.getVendorCompliance(this.selectedVendorId).subscribe({
      next: (res) => this.complianceRecords = res || [],
      error: () => this.complianceRecords = []
    });
  }

  private daysUntil(dateStr: string): number | null {
    if (!dateStr) return null;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return Math.ceil((new Date(dateStr).getTime() - today.getTime()) / 86400000);
  }

  certStatus(c: any): string {
    if (c.daysToExpiry === null) return c.status || 'Active';
    if (c.daysToExpiry < 0) return 'Expired';
    if (c.daysToExpiry <= 30) return 'Expiring Soon';
    return 'Active';
  }

  statusVariant(status: string): 'success' | 'warning' | 'danger' | 'default' {
    if (status === 'Active' || status === 'Compliant') return 'success';
    if (status === 'Expiring Soon' || status === 'Pending Verification') return 'warning';
    if (status === 'Expired' || status === 'Non-Compliant') return 'danger';
    return 'default';
  }

  addCertification(): void {
    this.errorMsg = '';
    this.actionMsg = '';
    const c = this.newCert;

    if (!c.certification_name || !c.certificate_number || !c.issuing_authority) {
      this.errorMsg = 'Certification name, certificate number and issuing authority are required.';
      return;
    }
    if (!c.issue_date || !c.expiry_date) {
      this.errorMsg = 'Issue date and expiry date are required.';
      return;
    }
    if (new Date(c.expiry_date) <= new Date(c.issue_date)) {
      this.errorMsg = 'Expiry date must be after the issue date.';
      return;
    }

    this.contractService.addCertification({
      ...c,
      vendor_id: Number(this.selectedVendorId)
    }).subscribe({
      next: () => {
        this.actionMsg = 'Certification added.';
        this.showCertForm = false;
        this.newCert = { certification_name: '', certificate_number: '', issuing_authority: '', issue_date: '', expiry_date: '' };
        this.loadRecords();
      },
      error: (err) => this.errorMsg = err.error?.detail || 'Could not add the certification.'
    });
  }

  deleteCertification(cert: any): void {
    if (!confirm(`Delete certification "${cert.certification_name}"?`)) return;
    this.contractService.deleteCertification(cert.id).subscribe({
      next: () => {
        this.actionMsg = 'Certification deleted.';
        this.loadRecords();
      },
      error: (err) => this.errorMsg = err.error?.detail || 'Could not delete the certification.'
    });
  }

  addCompliance(): void {
    this.errorMsg = '';
    this.actionMsg = '';

    this.contractService.recordCompliance({
      ...this.newCompliance,
      expiry_date: this.newCompliance.expiry_date || null,
      vendor_id: Number(this.selectedVendorId)
    }).subscribe({
      next: () => {
        this.actionMsg = 'Compliance record added.';
        this.showComplianceForm = false;
        this.newCompliance = { compliance_type: 'GST Compliance', status: 'Pending Verification', expiry_date: '', remarks: '' };
        this.loadRecords();
      },
      error: (err) => this.errorMsg = err.error?.detail || 'Could not add the compliance record.'
    });
  }

  updateComplianceStatus(record: any, status: string): void {
    this.errorMsg = '';
    this.actionMsg = '';
    this.contractService.updateComplianceStatus(record.id, status).subscribe({
      next: () => {
        this.actionMsg = `${record.compliance_type} marked ${status}.`;
        this.loadRecords();
      },
      error: (err) => this.errorMsg = err.error?.detail || 'Could not update the compliance status.'
    });
  }
}
