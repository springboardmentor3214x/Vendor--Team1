import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private readonly THEME_KEY = 'vrip-theme-preference';
  public isDarkMode = false;
}

const PLACEHOLDER_THEME_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderThemeService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_THEME_SERVICE_ROWS;
}
