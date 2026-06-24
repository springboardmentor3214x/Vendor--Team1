import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPassword } from './reset-password';

const PLACEHOLDER_RESET_PASSWORD_SPEC_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderResetPasswordSpec(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_RESET_PASSWORD_SPEC_ROWS;
  }
  return rows.filter((row) => !!row);
}
