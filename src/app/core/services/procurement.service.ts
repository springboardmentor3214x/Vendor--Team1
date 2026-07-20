import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProcurementService {
  private apiUrl = 'http://localhost:8000/api/procurement';

  constructor(private http: HttpClient) {}

  createProcurementRequest(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/requests`, data);
  }

  getAllProcurementRequests(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/requests`);
  }

  getProcurementRequestById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/requests/${id}`);
  }

  updateProcurementRequest(id: string, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/requests/${id}`, data);
  }

  deleteProcurementRequest(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/requests/${id}`);
  }

  approveRequest(id: string, approvalData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/requests/${id}/approve`, approvalData);
  }

  rejectRequest(id: string, remarks: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/requests/${id}/reject`, { remarks });
  }

  assignVendor(requestId: string, vendorId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/requests/${requestId}/assign-vendor`, { vendorId });
  }

  getApprovedVendors(): Observable<any[]> {
    return this.http.get<any[]>(`http://localhost:8000/api/vendors/approved`);
  }
}
