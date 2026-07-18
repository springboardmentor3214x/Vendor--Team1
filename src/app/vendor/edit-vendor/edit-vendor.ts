import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

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

  constructor(

    private route: ActivatedRoute,

    private router: Router,

    private vendorService: VendorService

  ) {}

  ngOnInit(): void {

    const id = Number(this.route.snapshot.paramMap.get('id'));

    const foundVendor = this.vendorService.getVendorById(id);

    if (foundVendor) {

      this.vendor = { ...foundVendor };

    } else {

      alert('Vendor not found.');

      this.router.navigate(['/vendors']);

    }

  }

  updateVendor(): void {

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

    this.vendorService.updateVendor(this.vendor);

    alert('Vendor updated successfully!');

    this.router.navigate(['/vendors']);

  }

  cancel(): void {

    this.router.navigate(['/vendors']);

  }

}