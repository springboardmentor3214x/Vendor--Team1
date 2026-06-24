import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CommunicationService {
  private apiUrl = '/communications';
  constructor(private http: HttpClient) {}
  getRegisteredRecipients(): Observable<any[]> {
    return this.http.get<any[]>('/users/recipients');
  }
  sendMessage(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/messages`, data);
  }
  sendMessageWithFile(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/messages/upload`, formData);
  }
  getMessages(vendorId?: number, poId?: number, contractId?: number, discussionId?: number, receiverId?: number): Observable<any[]> {
    let params = new HttpParams();
    if (vendorId) params = params.set('vendor_id', vendorId.toString());
    if (poId) params = params.set('po_id', poId.toString());
    if (contractId) params = params.set('contract_id', contractId.toString());
    if (discussionId) params = params.set('discussion_id', discussionId.toString());
    if (receiverId) params = params.set('receiver_id', receiverId.toString());

    return this.http.get<any[]>(`${this.apiUrl}/messages`, { params });
  }
}

const PLACEHOLDER_COMMUNICATION_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderCommunicationService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_COMMUNICATION_SERVICE_ROWS;
}
