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
}

const PLACEHOLDER_ADD_VENDOR_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderAddVendor(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_ADD_VENDOR_ROWS;
  }
  return rows.filter((row) => !!row);
}
