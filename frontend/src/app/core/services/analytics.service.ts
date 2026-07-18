import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AnalyticsService {
  private apiUrl = '/analytics';
  constructor(private http: HttpClient) {}
  getProcurementManagerDashboard(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/procurement-manager-dashboard`);
  }
}

const PLACEHOLDER_ANALYTICS_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderAnalyticsService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_ANALYTICS_SERVICE_ROWS;
}
