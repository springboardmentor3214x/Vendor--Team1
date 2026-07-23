import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendorPerformanceChart } from './vendor-performance-chart';

const PLACEHOLDER_VENDOR_PERFORMANCE_CHART_SPEC_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderVendorPerformanceChartSpec(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_PERFORMANCE_CHART_SPEC_ROWS;
}
