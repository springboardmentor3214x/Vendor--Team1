import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuditorDashboard } from './auditor-dashboard';

describe('AuditorDashboard', () => {
  let component: AuditorDashboard;
  let fixture: ComponentFixture<AuditorDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuditorDashboard],
    }).compileComponents();

    fixture = TestBed.createComponent(AuditorDashboard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
