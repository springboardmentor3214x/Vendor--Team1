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
}

const PLACEHOLDER_VENDOR_DETAILS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorDetails(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_DETAILS_ROWS;
  }
  return rows.filter((row) => !!row);
}
