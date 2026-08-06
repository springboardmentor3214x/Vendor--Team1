import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ReportsService {
  private apiUrl = '/reports';

  constructor(private http: HttpClient) {}

  getVendorPerformanceReport(category?: string, minReliability?: number): Observable<any[]> {
    let query = [];
    if (category && category !== 'All') query.push(`category=${category}`);
    if (minReliability) query.push(`min_reliability=${minReliability}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any[]>(`${this.apiUrl}/vendor-performance${queryString}`);
  }

  getProcurementReport(department?: string, status?: string): Observable<any> {
    let query = [];
    if (department && department !== 'All') query.push(`department=${department}`);
    if (status && status !== 'All') query.push(`status=${status}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any>(`${this.apiUrl}/procurement-summary${queryString}`);
  }

  getPOReport(status?: string, vendorId?: number): Observable<any[]> {
    let query = [];
    if (status && status !== 'All') query.push(`status=${status}`);
    if (vendorId) query.push(`vendor_id=${vendorId}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any[]>(`${this.apiUrl}/purchase-orders${queryString}`);
  }

  getComplianceReport(status?: string): Observable<any> {
    let query = [];
    if (status && status !== 'All') query.push(`status=${status}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any>(`${this.apiUrl}/compliance${queryString}`);
  }

  getContractReport(status?: string): Observable<any[]> {
    let query = [];
    if (status && status !== 'All') query.push(`status=${status}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any[]>(`${this.apiUrl}/contracts${queryString}`);
  }

  getExecutiveSummaryReport(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/executive-summary`);
  }

  downloadPDF(reportType: string = 'vendor-performance'): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/export/pdf?report_type=${reportType}`, { responseType: 'blob' });
  }

  downloadExcel(reportType: string = 'vendor-performance'): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/export/excel?report_type=${reportType}`, { responseType: 'blob' });
  }
}
