import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ProcurementService {
  private apiUrl = '/procurements';
  constructor(private http: HttpClient) {}
  getProcurementDashboard(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/dashboard`);
  }
  createProcurementRequest(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data);
  }
  getAllProcurementRequests(filters?: { department?: string; status?: string; priority?: string; keyword?: string }): Observable<any[]> {
    let params = new HttpParams();
    if (filters?.department) params = params.set('department', filters.department);
    if (filters?.status) params = params.set('status', filters.status);
    if (filters?.priority) params = params.set('priority', filters.priority);
    if (filters?.keyword) params = params.set('keyword', filters.keyword);

    return this.http.get<any[]>(`${this.apiUrl}/`, { params });
  }
  getProcurementRequestById(id: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }
  getProcurementStatusHistory(id: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/${id}/history`);
  }
  updateProcurementRequest(id: string | number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }
  deleteProcurementRequest(id: string | number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
  approveRequest(id: string | number, remarks: string = 'Approved'): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/approve`, { remarks });
  }
  rejectRequest(id: string | number, remarks: string = 'Rejected'): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/reject`, { remarks });
  }
  sendBackRequest(id: string | number, remarks: string = 'Needs modification'): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/send-back`, { remarks });
  }
}

const PLACEHOLDER_PROCUREMENT_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderProcurementService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PROCUREMENT_SERVICE_ROWS;
}
