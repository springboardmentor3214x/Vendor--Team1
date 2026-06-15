import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Navbar } from './navbar';

const PLACEHOLDER_NAVBAR_SPEC_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderNavbarSpec(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_NAVBAR_SPEC_ROWS;
  }
  return rows.filter((row) => !!row);
}
