import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PerformanceService {
  private apiUrl = '/performance';
  constructor(private http: HttpClient) {}
  getDashboardStats(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/dashboard`);
  }
  getVendorMetrics(vendorId: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/metrics/${vendorId}`);
  }
  getVendorRankings(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/rankings`);
  }
}

const PLACEHOLDER_PERFORMANCE_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderPerformanceService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PERFORMANCE_SERVICE_ROWS;
}
