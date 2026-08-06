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

  // Purchase Order APIs
  createPurchaseOrder(data: any): Observable<any> {
    return this.http.post('/purchase-orders/', data);
  }

  getAllPurchaseOrders(): Observable<any[]> {
    return this.http.get<any[]>('/purchase-orders/');
  }

  getPurchaseOrderById(id: string | number): Observable<any> {
    return this.http.get<any>(`/purchase-orders/${id}`);
  }

  updatePOStatus(id: string | number, status: string): Observable<any> {
    return this.http.put(`/purchase-orders/${id}/status?status=${status}`, {});
  }

  // Order Tracking APIs
  getAllOrderTracking(): Observable<any[]> {
    return this.http.get<any[]>('/order-tracking/');
  }

  getOrderTrackingByPO(poId: string | number): Observable<any> {
    return this.http.get<any>(`/order-tracking/${poId}`);
  }

  updateOrderTracking(poId: string | number, data: any): Observable<any> {
    return this.http.put(`/order-tracking/${poId}`, data);
  }

  // Invoice APIs
  uploadInvoice(formData: FormData): Observable<any> {
    return this.http.post('/invoices/upload', formData);
  }

  getAllInvoices(): Observable<any[]> {
    return this.http.get<any[]>('/invoices/');
  }

  verifyInvoice(invoiceId: string | number, action: string, remarks?: string): Observable<any> {
    return this.http.post(`/invoices/${invoiceId}/verify`, { action, remarks });
  }
}
