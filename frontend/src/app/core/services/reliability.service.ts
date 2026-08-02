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
}

const PLACEHOLDER_RELIABILITY_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderReliabilityService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_RELIABILITY_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
