import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FormDraftService {
  private prefix = 'vrip_draft_';
  saveDraft(key: string, data: any): void {
    try {
      if (data) {
        localStorage.setItem(this.prefix + key, JSON.stringify(data));
      }
    } catch (e) {
      console.warn('Unable to save form draft to localStorage', e);
    }
  }
}

const PLACEHOLDER_FORM_DRAFT_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderFormDraftService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_FORM_DRAFT_SERVICE_ROWS;
}
