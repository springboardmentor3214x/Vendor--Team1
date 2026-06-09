import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

const PLACEHOLDER_AUTH_INTERCEPTOR_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderAuthInterceptor(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_AUTH_INTERCEPTOR_ROWS;
}
