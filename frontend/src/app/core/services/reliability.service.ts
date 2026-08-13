import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ReliabilityService {
  private apiUrl = '/reliability';

  constructor(private http: HttpClient) {}

  getDashboard(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/dashboard`);
  }

  getDetails(vendorId: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/details/${vendorId}`);
  }

  getRankings(category?: string): Observable<any[]> {
    const url = category ? `${this.apiUrl}/rankings?category=${category}` : `${this.apiUrl}/rankings`;
    return this.http.get<any[]>(url);
  }

  getRiskAssessment(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/risk-assessment`);
  }

  getTrends(vendorId: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/trends/${vendorId}`);
  }

  getRecommendations(category?: string): Observable<any[]> {
    const url = category ? `${this.apiUrl}/recommendations?category=${category}` : `${this.apiUrl}/recommendations`;
    return this.http.get<any[]>(url);
  }
}
