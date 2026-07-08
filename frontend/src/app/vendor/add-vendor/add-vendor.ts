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

    name: '',

    category: '',

    email: '',

    phone: '',

    gst: '',

    rating: 5,

    status: 'Pending'

  };

  constructor(

    private vendorService: VendorService,

    private router: Router

  ) {}

  saveVendor() {

    this.vendorService.addVendor(this.vendor);

    this.router.navigate(['/vendors']);

  }

}