import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrderTracking } from './order-tracking';

const PLACEHOLDER_ORDER_TRACKING_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderOrderTrackingSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_ORDER_TRACKING_SPEC_ROWS;
}
