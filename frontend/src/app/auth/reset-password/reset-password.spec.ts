import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPassword } from './reset-password';

const PLACEHOLDER_RESET_PASSWORD_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderResetPasswordSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_RESET_PASSWORD_SPEC_ROWS;
}
