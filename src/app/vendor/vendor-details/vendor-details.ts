import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

@Component({
  selector: 'app-vendor-details',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  templateUrl: './vendor-details.html',
  styleUrl: './vendor-details.css'
})
export class VendorDetails implements OnInit {

  vendor?: Vendor;

  constructor(

    private route: ActivatedRoute,

    private vendorService: VendorService

  ) {}

  ngOnInit(): void {

    const id = Number(this.route.snapshot.paramMap.get('id'));

    this.vendor = this.vendorService
      .getVendors()
      .find(v => v.id === id);

  }

}