import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { forkJoin, of, catchError } from 'rxjs';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';
import { VENDOR_CATEGORIES } from '../../core/vendor-categories';
import { VENDOR_DOCUMENT_SLOTS, validateDocumentFile } from '../../core/vendor-documents';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-add-vendor',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './add-vendor.html',
  styleUrls: ['./add-vendor.css']
})
export class AddVendor {

  vendor: Vendor = {

    id: 0,

    companyName: '',

    category: '',

    contactPerson: '',

    designation: '',

    email: '',

    phone: '',

    alternatePhone: '',

    gst: '',

    pan: '',

    companyRegistrationNumber: '',

    addressLine1: '',

    addressLine2: '',

    city: '',

    state: '',

    country: '',

    pincode: '',

    website: '',

    description: '',

    bankAccountNumber: '',

    ifscCode: '',

    paymentTerms: '',

    gstCertificate: '',
    gstCertificateUrl: '',

    panCard: '',
    panCardUrl: '',

    registrationCertificate: '',
    registrationCertificateUrl: '',

    isoCertificate: '',
    isoCertificateUrl: '',

    otherDocument: '',
    otherDocumentUrl: '',

    rating: 5,

    status: 'Pending',

    approvalStatus: 'Pending'

  };

  constructor(

    private vendorService: VendorService,

    private router: Router

  ) {}

  readonly categories = VENDOR_CATEGORIES;
  readonly documentSlots = VENDOR_DOCUMENT_SLOTS;

  private selectedFiles = new Map<string, File>();

  errorMsg = '';
  fileError = '';
  saving = false;

  onFileSelected(event: Event, documentType: string): void {

    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {
      return;
    }

    const file = input.files[0];

    this.fileError = validateDocumentFile(file);
    if (this.fileError) {
      input.value = '';
      return;
    }

    this.selectedFiles.set(documentType, file);

  }

  selectedFileName(documentType: string): string {
    return this.selectedFiles.get(documentType)?.name || '';
  }

  removeFile(documentType: string): void {
    this.selectedFiles.delete(documentType);
  }

  saveVendor(): void {

    this.errorMsg = '';

    const missing = this.validate();
    if (missing) {
      this.errorMsg = missing;
      return;
    }

    this.saving = true;

    this.vendorService.addVendor(this.vendor).subscribe({
      next: (created) => {
        this.uploadSelectedDocuments(created?.id);
      },
      error: (error) => {
        this.saving = false;

        this.errorMsg = error.error?.detail || 'The vendor could not be saved. Please try again.';
      }
    });

  }

  private uploadSelectedDocuments(vendorId?: number): void {

    const uploads = Array.from(this.selectedFiles.entries());

    if (!vendorId || uploads.length === 0) {
      this.saving = false;
      this.router.navigate(['/vendors']);
      return;
    }

    forkJoin(
      uploads.map(([documentType, file]) =>
        this.vendorService.uploadDocument(vendorId, documentType, file).pipe(
          catchError(() => of({ failed: documentType }))
        )
      )
    ).subscribe(results => {
      this.saving = false;
      const failed = results
        .filter((r: any) => r && r.failed)
        .map((r: any) => r.failed);

      if (failed.length > 0) {
        this.errorMsg =
          `The vendor was saved, but these documents could not be uploaded: ${failed.join(', ')}. ` +
          `You can attach them from the Edit Vendor page.`;
        return;
      }

      this.router.navigate(['/vendors']);
    });

  }

  private validate(): string {
    const v = this.vendor;
    if (!v.companyName?.trim()) return 'Company Name is required.';
    if (!v.category?.trim()) return 'Vendor Category is required.';
    if (!v.contactPerson?.trim()) return 'Contact Person Name is required.';
    if (!v.email?.trim()) return 'Email Address is required.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) return 'Enter a valid email address.';
    if (!v.phone?.trim()) return 'Phone Number is required.';
    if (!/^\d{10}$/.test(v.phone.replace(/\D/g, '').slice(-10))) return 'Enter a valid 10-digit phone number.';
    if (v.pincode && !/^\d{6}$/.test(v.pincode)) return 'Pincode must be 6 digits.';
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

  cancel(): void {

    this.router.navigate(['/vendors']);

  }

}