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

  getQualityRecords(vendorId: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/quality/${vendorId}`);
  }

  recordCommunication(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/communication`, data);
  }

  getCommunicationRecords(vendorId: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/communication/${vendorId}`);
  }

  submitServiceRating(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/service-rating`, data);
  }

  getServiceRatings(vendorId: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/service-rating/${vendorId}`);
  }
}
