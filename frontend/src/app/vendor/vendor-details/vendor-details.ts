import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';
import { VendorDocument } from '../../core/vendor-documents';

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

  documents: VendorDocument[] = [];
  documentsLoading = false;
  documentError = '';

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
        if (this.vendor) {
          this.loadDocuments(this.vendor.id);
        }
        this.cdr.markForCheck();
      },
      error: () => {
        this.vendor = undefined;
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }

  private loadDocuments(vendorId: number): void {
    this.documentsLoading = true;
    this.vendorService.getVendorDocuments(vendorId).subscribe({
      next: (docs) => {
        this.documents = docs || [];
        this.documentsLoading = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.documents = [];
        this.documentsLoading = false;
        this.documentError = 'Could not load the uploaded documents.';
        this.cdr.markForCheck();
      }
    });
  }

  viewDocument(doc: VendorDocument): void {
    if (!this.vendor) {
      return;
    }
    this.documentError = '';
    this.vendorService.downloadDocument(this.vendor.id, doc.id).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        window.open(url, '_blank');

        setTimeout(() => URL.revokeObjectURL(url), 60000);
      },
      error: (err) => {
        this.documentError = err.error?.detail || 'The document could not be opened.';
        this.cdr.markForCheck();
      }
    });
  }

}
