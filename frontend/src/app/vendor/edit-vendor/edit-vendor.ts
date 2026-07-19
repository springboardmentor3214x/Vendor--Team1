import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';
import { VENDOR_CATEGORIES } from '../../core/vendor-categories';
import {
  VENDOR_DOCUMENT_SLOTS,
  VendorDocument,
  validateDocumentFile
} from '../../core/vendor-documents';

const VENDOR_STATUSES = ['Active', 'Pending', 'Inactive', 'Suspended', 'Rejected'];

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-edit-vendor',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './edit-vendor.html',
  styleUrls: ['./edit-vendor.css']
})
export class EditVendor implements OnInit {

  vendor!: Vendor;
  loading = true;
  saving = false;
  errorMsg = '';

  readonly categories = VENDOR_CATEGORIES;
  readonly statuses = VENDOR_STATUSES;
  readonly documentSlots = VENDOR_DOCUMENT_SLOTS;

  documents: VendorDocument[] = [];
  documentError = '';
  documentMsg = '';
  uploadingType = '';

  constructor(

    private route: ActivatedRoute,

    private router: Router,

    private vendorService: VendorService

  ) {}

  ngOnInit(): void {

    const id = Number(this.route.snapshot.paramMap.get('id'));

    this.vendorService.loadVendors().subscribe({
      next: (vendors) => {
        const found = vendors.find(v => v.id === id);
        this.loading = false;
        if (found) {
          this.vendor = { ...found };
          this.loadDocuments();
        } else {
          this.errorMsg = 'Vendor not found.';
          this.router.navigate(['/vendors']);
        }
      },
      error: () => {
        this.loading = false;
        this.errorMsg = 'Could not load the vendor. Please try again.';
      }
    });

  }

  updateVendor(): void {

    this.errorMsg = '';

    const problem = this.validate();
    if (problem) {
      this.errorMsg = problem;
      return;
    }

    this.saving = true;

    this.vendorService.updateVendor(this.vendor).subscribe({
      next: () => {
        this.saving = false;
        this.router.navigate(['/vendors']);
      },
      error: (error) => {
        this.saving = false;
        this.errorMsg = error.error?.detail || 'The vendor could not be updated. Please try again.';
      }
    });

  }

  private validate(): string {
    const v = this.vendor;
    if (!v.companyName?.trim()) return 'Company Name is required.';
    if (!v.category?.trim()) return 'Vendor Category is required.';
    if (!v.contactPerson?.trim()) return 'Contact Person is required.';
    if (!v.email?.trim()) return 'Email Address is required.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) return 'Enter a valid email address.';
    if (!v.phone?.trim()) return 'Phone Number is required.';
    if (v.phone.replace(/\D/g, '').length < 10) return 'Phone Number should be at least 10 digits.';
    if (v.gst && !/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]{3}$/i.test(v.gst)) {
      return 'GST Number format is invalid (example: 27AABCT1234F1Z5).';
    }
    if (v.pan && !/^[A-Z]{5}[0-9]{4}[A-Z]$/i.test(v.pan)) {
      return 'PAN Number format is invalid (example: AABCT1234F).';
    }
    if (v.ifscCode && !/^[A-Z]{4}0[A-Z0-9]{6}$/i.test(v.ifscCode)) {
      return 'IFSC Code format is invalid (example: HDFC0001234).';
    }
    return '';
  }

  approveVendor(): void {
    if (!this.vendor?.id) return;
    this.errorMsg = '';
    this.vendorService.approveVendor(this.vendor.id).subscribe({
      next: () => this.router.navigate(['/vendors']),
      error: (error) => {
        this.errorMsg = error.error?.detail || 'The vendor could not be approved.';
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/vendors']);
  }

  get isLegacyCategory(): boolean {
    return !!this.vendor?.category && !this.categories.includes(this.vendor.category);
  }

  private loadDocuments(): void {
    this.vendorService.getVendorDocuments(this.vendor.id).subscribe({
      next: (docs) => this.documents = docs || [],
      error: () => this.documentError = 'Could not load the uploaded documents.'
    });
  }

  existingDocument(documentType: string): VendorDocument | undefined {
    return this.documents.find(d => d.document_type === documentType);
  }

  onFileSelected(event: Event, documentType: string): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) {
      return;
    }

    const file = input.files[0];
    this.documentError = '';
    this.documentMsg = '';

    const problem = validateDocumentFile(file);
    if (problem) {
      this.documentError = problem;
      input.value = '';
      return;
    }

    this.uploadingType = documentType;
    this.vendorService.uploadDocument(this.vendor.id, documentType, file).subscribe({
      next: () => {
        this.uploadingType = '';
        this.documentMsg = `${documentType} uploaded successfully.`;
        this.loadDocuments();
      },
      error: (err) => {
        this.uploadingType = '';
        this.documentError = err.error?.detail || `${documentType} could not be uploaded.`;
      }
    });

    input.value = '';
  }

  viewDocument(doc: VendorDocument): void {
    this.documentError = '';
    this.vendorService.downloadDocument(this.vendor.id, doc.id).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        window.open(url, '_blank');
        setTimeout(() => URL.revokeObjectURL(url), 60000);
      },
      error: (err) => {
        this.documentError = err.error?.detail || 'The document could not be opened.';
      }
    });
  }

  deleteDocument(doc: VendorDocument): void {
    if (!confirm(`Remove "${doc.file_name}"?`)) {
      return;
    }
    this.documentError = '';
    this.documentMsg = '';
    this.vendorService.deleteVendorDocument(this.vendor.id, doc.id).subscribe({
      next: () => {
        this.documentMsg = `${doc.document_type} removed.`;
        this.loadDocuments();
      },
      error: (err) => {
        this.documentError = err.error?.detail || 'The document could not be removed.';
      }
    });
  }
}