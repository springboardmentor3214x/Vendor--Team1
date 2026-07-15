import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

@Component({
  selector: 'app-add-vendor',
  standalone: true,
  imports: [FormsModule],
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

    rating: 5,

    status: 'Pending',

    approvalStatus: 'Pending'

  };

  constructor(

    private vendorService: VendorService,

    private router: Router

  ) {}

  saveVendor(): void {

    if (!this.vendor.companyName.trim()) {

      alert('Company Name is required');

      return;

    }

    if (!this.vendor.category.trim()) {

      alert('Vendor Category is required');

      return;

    }

    if (!this.vendor.contactPerson.trim()) {

      alert('Contact Person is required');

      return;

    }

    if (!this.vendor.email.trim()) {

      alert('Email Address is required');

      return;

    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(this.vendor.email)) {

      alert('Enter a valid Email Address');

      return;

    }

    if (!this.vendor.phone.trim()) {

      alert('Phone Number is required');

      return;

    }

    if (this.vendor.phone.length < 10) {

      alert('Phone Number should be at least 10 digits');

      return;

    }

    if (!this.vendor.gst.trim()) {

      alert('GST Number is required');

      return;

    }

    if (!this.vendor.pan?.trim()) {

      alert('PAN Number is required');

      return;

    }

    this.vendorService.addVendor(this.vendor);

    alert('Vendor added successfully!');

    this.router.navigate(['/vendors']);

  }

  cancel(): void {

    this.router.navigate(['/vendors']);

  }

}