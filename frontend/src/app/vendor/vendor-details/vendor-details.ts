import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';

@Component({
  selector: 'app-vendor-details',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Button,
    Badge
  ],
  templateUrl: './vendor-details.html',
  styleUrls: ['./vendor-details.css']
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

  viewDocument(url?: string): void {

    if (url) {

      window.open(url, '_blank');

    }

  }

}