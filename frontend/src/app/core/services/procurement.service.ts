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

  dispatchRequest(id: string | number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/dispatch`, {});
  }

  deliverRequest(id: string | number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/deliver`, {});
  }

  completeRequest(id: string | number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/complete`, {});
  }

  placeOrder(id: string | number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/place-order`, {});
  }

  assignVendor(requestId: string | number, vendorId: string | number, acknowledgeRisk = false): Observable<any> {
    return this.http.post(`${this.apiUrl}/${requestId}/assign-vendor`, {
      vendor_id: Number(vendorId),
      acknowledge_risk: acknowledgeRisk
    });
  }

  getApprovedVendors(): Observable<any[]> {
    return this.http.get<any[]>('/vendors/approved');
  }

  downloadPurchaseOrderPdf(poId: string | number): Observable<Blob> {
    return this.http.get(`/purchase-orders/${poId}/pdf`, { responseType: 'blob' });
  }

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

  getAllOrderTracking(): Observable<any[]> {
    return this.http.get<any[]>('/order-tracking/');
  }

  getOrderTrackingByPO(poId: string | number): Observable<any> {
    return this.http.get<any>(`/order-tracking/${poId}`);
  }

  updateOrderTracking(poId: string | number, data: any): Observable<any> {
    return this.http.put(`/order-tracking/${poId}`, data);
  }

  uploadInvoice(formData: FormData): Observable<any> {
    return this.http.post('/invoices/upload', formData);
  }

  createInvoiceJson(data: any): Observable<any> {
    return this.http.post('/invoices/', data);
  }

  getAllInvoices(): Observable<any[]> {
    return this.http.get<any[]>('/invoices/');
  }

  getInvoiceById(id: string | number): Observable<any> {
    return this.http.get<any>(`/invoices/${id}`);
  }

  verifyInvoice(invoiceId: string | number, action: string, remarks?: string): Observable<any> {
    return this.http.post(`/invoices/${invoiceId}/verify`, { action, remarks });
  }
}
