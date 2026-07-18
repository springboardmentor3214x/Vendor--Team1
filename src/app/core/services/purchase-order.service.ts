import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PurchaseOrderService {
  private apiUrl = 'http://localhost:8000/api/purchase-orders';

  constructor(private http: HttpClient) {}

  createPurchaseOrder(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}`, data);
  }

  getPurchaseOrders(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}`);
  }

  getPurchaseOrderById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  updatePurchaseOrder(id: string, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }

  updateDeliveryStatus(id: string, status: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/delivery-status`, { status });
  }

  trackPurchaseOrder(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}/tracking`);
  }
}
