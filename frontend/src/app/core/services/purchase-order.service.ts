import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PurchaseOrderService {
  private apiUrl = '/procurements/purchase-orders';
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
}

const PLACEHOLDER_PURCHASE_ORDER_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderPurchaseOrderService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PURCHASE_ORDER_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
