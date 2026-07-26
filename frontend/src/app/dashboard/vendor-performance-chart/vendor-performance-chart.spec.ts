import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendorPerformanceChart } from './vendor-performance-chart';

const PLACEHOLDER_VENDOR_PERFORMANCE_CHART_SPEC_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderVendorPerformanceChartSpec(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_PERFORMANCE_CHART_SPEC_ROWS;
  }
  return rows.filter((row) => !!row);
}
