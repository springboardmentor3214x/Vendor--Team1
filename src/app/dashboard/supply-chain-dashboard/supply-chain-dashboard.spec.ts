import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SupplyChainDashboard } from './supply-chain-dashboard';

describe('SupplyChainDashboard', () => {
  let component: SupplyChainDashboard;
  let fixture: ComponentFixture<SupplyChainDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SupplyChainDashboard],
    }).compileComponents();

    fixture = TestBed.createComponent(SupplyChainDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
