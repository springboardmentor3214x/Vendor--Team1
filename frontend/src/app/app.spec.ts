import { TestBed } from '@angular/core/testing';
import { App } from './app';

const PLACEHOLDER_APP_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderAppSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_APP_SPEC_ROWS;
}
