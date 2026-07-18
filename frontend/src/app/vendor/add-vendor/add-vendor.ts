import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

@Component({
  selector: 'app-add-vendor',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './add-vendor.html',
  styleUrl: './add-vendor.css'
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

  onFileSelected(event: Event, field: keyof Vendor): void {

    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {

      return;

    }

    const file = input.files[0];

    const fileName = file.name;

    const fileUrl = URL.createObjectURL(file);

    switch (field) {

      case 'gstCertificate':

        this.vendor.gstCertificate = fileName;
        this.vendor.gstCertificateUrl = fileUrl;
        break;

      case 'panCard':

        this.vendor.panCard = fileName;
        this.vendor.panCardUrl = fileUrl;
        break;

      case 'registrationCertificate':

        this.vendor.registrationCertificate = fileName;
        this.vendor.registrationCertificateUrl = fileUrl;
        break;

      case 'isoCertificate':

        this.vendor.isoCertificate = fileName;
        this.vendor.isoCertificateUrl = fileUrl;
        break;

      case 'otherDocument':

        this.vendor.otherDocument = fileName;
        this.vendor.otherDocumentUrl = fileUrl;
        break;

    }

  }

  viewDocument(url?: string): void {

    if (url) {

      window.open(url, '_blank');

    }

  }

  saveVendor(): void {

    this.vendorService.addVendor(this.vendor);

    this.router.navigate(['/vendors']);

  }

  cancel(): void {

    this.router.navigate(['/vendors']);

  }

}