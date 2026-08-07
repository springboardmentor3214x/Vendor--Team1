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
  getDraft<T>(key: string): T | null {
    try {
      const item = localStorage.getItem(this.prefix + key);
      return item ? JSON.parse(item) : null;
    } catch (e) {
      console.warn('Unable to read form draft from localStorage', e);
      return null;
    }
  }
  clearDraft(key: string): void {
    try {
      localStorage.removeItem(this.prefix + key);
    } catch (e) {
      console.warn('Unable to clear form draft from localStorage', e);
    }
  }
}

const PLACEHOLDER_FORM_DRAFT_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderFormDraftService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_FORM_DRAFT_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
