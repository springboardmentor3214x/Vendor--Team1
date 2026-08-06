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

  getVendorDashboard(vendorId: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/vendor-dashboard/${vendorId}`);
  }

  getAdminDashboard(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/admin-dashboard`);
  }
}
