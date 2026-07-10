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
}

const PLACEHOLDER_ADD_VENDOR_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderAddVendor(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_ADD_VENDOR_ROWS;
}
