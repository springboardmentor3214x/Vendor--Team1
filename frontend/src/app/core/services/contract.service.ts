import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ContractService {
  private apiUrl = '/contracts';
  constructor(private http: HttpClient) {}
  getContracts(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`);
  }
  getExpiringContracts(days: number = 90): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/expiring?days=${days}`);
  }
  downloadContractDocument(id: string | number): Observable<Blob> {
    return this.http.get(`${this.apiUrl}${id}/document`, { responseType: 'blob' });
  }
  getContractById(id: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }
}

const PLACEHOLDER_CONTRACT_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderContractService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_CONTRACT_SERVICE_ROWS;
}
