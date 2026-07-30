import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ReportFilters {
  category?: string;
  department?: string;
  status?: string;
  vendorId?: number;
  minReliability?: number;
  startDate?: string;
  endDate?: string;
  expiringWithinDays?: number;
}

@Injectable({ providedIn: 'root' })
export class ReportsService {
  private apiUrl = '/reports';
  constructor(private http: HttpClient) {}
  private buildParams(filters: ReportFilters = {}): HttpParams {
    let params = new HttpParams();
    const set = (key: string, value: any) => {
      if (value === undefined || value === null || value === '' || value === 'All') return;
      params = params.set(key, String(value));
    };

    set('category', filters.category);
    set('department', filters.department);
    set('status', filters.status);
    set('vendor_id', filters.vendorId);
    set('min_reliability', filters.minReliability);
    set('start_date', filters.startDate);
    set('end_date', filters.endDate);
    set('expiring_within_days', filters.expiringWithinDays);

    return params;
  }
  getVendorPerformanceReport(filters: ReportFilters = {}): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/vendor-performance`, { params: this.buildParams(filters) });
  }
  getProcurementReport(filters: ReportFilters = {}): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/procurement-summary`, { params: this.buildParams(filters) });
  }
  getPOReport(filters: ReportFilters = {}): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/purchase-orders`, { params: this.buildParams(filters) });
  }
  getComplianceReport(filters: ReportFilters = {}): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/compliance`, { params: this.buildParams(filters) });
  }
}

const PLACEHOLDER_REPORTS_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderReportsService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_REPORTS_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
