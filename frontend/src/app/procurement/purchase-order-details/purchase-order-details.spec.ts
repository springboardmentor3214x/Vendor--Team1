import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PurchaseOrderDetails } from './purchase-order-details';

const PLACEHOLDER_PURCHASE_ORDER_DETAILS_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderPurchaseOrderDetailsSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PURCHASE_ORDER_DETAILS_SPEC_ROWS;
}
