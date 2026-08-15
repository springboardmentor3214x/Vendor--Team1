import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProcurementApproval } from './procurement-approval';

describe('ProcurementApproval', () => {
  let component: ProcurementApproval;
  let fixture: ComponentFixture<ProcurementApproval>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProcurementApproval],
    }).compileComponents();

    fixture = TestBed.createComponent(ProcurementApproval);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

const PLACEHOLDER_PROCUREMENT_APPROVAL_SPEC_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderProcurementApprovalSpec(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_PROCUREMENT_APPROVAL_SPEC_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
