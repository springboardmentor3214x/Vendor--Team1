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
}

const PLACEHOLDER_PURCHASE_ORDER_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderPurchaseOrderService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PURCHASE_ORDER_SERVICE_ROWS;
}
