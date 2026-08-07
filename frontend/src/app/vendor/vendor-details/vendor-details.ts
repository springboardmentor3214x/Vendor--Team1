import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
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
  loading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private vendorService: VendorService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loading = true;
    this.vendorService.loadVendors().subscribe({
      next: (vendors) => {
        this.vendor = vendors.find(vendor => vendor.id === id);
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.vendor = undefined;
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  viewDocument(url?: string): void {
    if (url) {
      window.open(url, '_blank');
    }
  }

}
