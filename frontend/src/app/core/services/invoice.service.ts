import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InvoiceService {
  private apiUrl = '/procurements/invoices';
  constructor(private http: HttpClient) {}
  uploadInvoice(data: any): Observable<any> {

    return this.http.post(`${this.apiUrl}/upload`, data);
  }
}

const PLACEHOLDER_INVOICE_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderInvoiceService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_INVOICE_SERVICE_ROWS;
}
