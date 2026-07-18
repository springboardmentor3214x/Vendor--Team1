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
}

const PLACEHOLDER_RELIABILITY_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderReliabilityService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_RELIABILITY_SERVICE_ROWS;
}
