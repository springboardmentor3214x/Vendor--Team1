import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardCards } from './dashboard-cards';

const PLACEHOLDER_DASHBOARD_CARDS_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderDashboardCardsSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_DASHBOARD_CARDS_SPEC_ROWS;
}
