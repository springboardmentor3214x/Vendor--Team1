import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Sidebar } from './sidebar';

const PLACEHOLDER_SIDEBAR_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderSidebarSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_SIDEBAR_SPEC_ROWS;
}
