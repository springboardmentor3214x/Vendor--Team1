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
  getVendorHistory(vendorId: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/history/${vendorId}`);
  }
  recordDelivery(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/delivery`, data);
  }
  getDeliveryRecords(vendorId: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/delivery/${vendorId}`);
  }
  recordQuality(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/quality`, data);
  }
}

const PLACEHOLDER_PERFORMANCE_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderPerformanceService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PERFORMANCE_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
