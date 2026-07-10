import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddVendor } from './add-vendor';

const PLACEHOLDER_ADD_VENDOR_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderAddVendorSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_ADD_VENDOR_SPEC_ROWS;
}
