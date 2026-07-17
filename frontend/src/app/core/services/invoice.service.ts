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

  verifyInvoice(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/verify`, {});
  }

  updatePaymentStatus(id: string, status: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/payment-status`, { status });
  }

  getInvoices(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}`);
  }

  getInvoiceDetails(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }
}
