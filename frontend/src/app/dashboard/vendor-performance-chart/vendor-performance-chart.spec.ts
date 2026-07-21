import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VendorPerformanceChart } from './vendor-performance-chart';

describe('VendorPerformanceChart', () => {
  let component: VendorPerformanceChart;
  let fixture: ComponentFixture<VendorPerformanceChart>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VendorPerformanceChart],
    }).compileComponents();

    fixture = TestBed.createComponent(VendorPerformanceChart);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
