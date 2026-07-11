import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { VendorService } from '../../services/vendor';
import { Vendor } from '../../services/vendor.model';
import { VENDOR_CATEGORIES } from '../../core/vendor-categories';
import {
  VENDOR_DOCUMENT_SLOTS,
  VendorDocument,
  validateDocumentFile
} from '../../core/vendor-documents';

const VENDOR_STATUSES = ['Active', 'Pending', 'Inactive', 'Suspended', 'Rejected'];

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
  loading = true;
  saving = false;
  errorMsg = '';
  readonly categories = VENDOR_CATEGORIES;
  readonly statuses = VENDOR_STATUSES;
  readonly documentSlots = VENDOR_DOCUMENT_SLOTS;
  documents: VendorDocument[] = [];
}

const PLACEHOLDER_EDIT_VENDOR_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderEditVendor(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_EDIT_VENDOR_ROWS;
}
