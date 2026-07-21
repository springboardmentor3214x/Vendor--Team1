import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ProcurementService {
  private apiUrl = '/procurements';

  constructor(private http: HttpClient) {}

  createProcurementRequest(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data);
  }

  getAllProcurementRequests(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`);
  }

  getProcurementRequestById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  updateProcurementRequest(id: string, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }

  deleteProcurementRequest(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  approveRequest(id: string, approvalData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/approve`, approvalData);
  }

  rejectRequest(id: string, remarks: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/reject`, { remarks });
  }

  dispatchRequest(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/dispatch`, {});
  }

  deliverRequest(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/deliver`, {});
  }

  completeRequest(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/complete`, {});
  }

  placeOrder(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/place-order`, {});
  }

  assignVendor(requestId: string, vendorId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${requestId}/assign-vendor`, {
      vendor_id: Number(vendorId)
    });
  }

  getApprovedVendors(): Observable<any[]> {
    return this.http.get<any[]>('/vendors/?status=Active&limit=200');
  }
}
