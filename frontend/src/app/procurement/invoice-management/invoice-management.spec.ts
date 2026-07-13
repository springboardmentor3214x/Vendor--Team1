import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoiceManagement } from './invoice-management';

const PLACEHOLDER_INVOICE_MANAGEMENT_SPEC_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderInvoiceManagementSpec(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_INVOICE_MANAGEMENT_SPEC_ROWS;
  }
  return rows.filter((row) => !!row);
}
