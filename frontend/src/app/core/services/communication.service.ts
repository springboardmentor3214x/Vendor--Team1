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

  createDiscussion(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/discussions`, data);
  }

  getDiscussions(vendorId?: number, poId?: number): Observable<any[]> {
    let params = new HttpParams();
    if (vendorId) params = params.set('vendor_id', vendorId.toString());
    if (poId) params = params.set('po_id', poId.toString());
    return this.http.get<any[]>(`${this.apiUrl}/discussions`, { params });
  }

  uploadFile(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/files/upload`, formData);
  }

  getFiles(filters: {
    vendorId?: number; poId?: number; contractId?: number;
    procurementId?: number; discussionId?: number;
  } = {}): Observable<any[]> {
    let params = new HttpParams();
    if (filters.vendorId) params = params.set('vendor_id', String(filters.vendorId));
    if (filters.poId) params = params.set('po_id', String(filters.poId));
    if (filters.contractId) params = params.set('contract_id', String(filters.contractId));
    if (filters.procurementId) params = params.set('procurement_id', String(filters.procurementId));
    if (filters.discussionId) params = params.set('discussion_id', String(filters.discussionId));
    return this.http.get<any[]>(`${this.apiUrl}/files`, { params });
  }

  downloadSharedFile(fileId: number): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/files/${fileId}/download`, { responseType: 'blob' });
  }

  downloadMessageAttachment(messageId: number): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/messages/${messageId}/attachment`, { responseType: 'blob' });
  }

  markMessagesRead(body: { message_ids?: number[]; vendor_id?: number; discussion_id?: number } = {}): Observable<any> {
    return this.http.post(`${this.apiUrl}/messages/mark-read`, body);
  }

  getUnreadMessageCount(): Observable<{ unread_count: number }> {
    return this.http.get<{ unread_count: number }>(`${this.apiUrl}/messages/unread-count`);
  }

  getActivityLogs(moduleName?: string, limit: number = 100): Observable<any[]> {
    let url = `${this.apiUrl}/activity-logs?limit=${limit}`;
    if (moduleName && moduleName !== 'All') {
      url += `&module=${moduleName}`;
    }
    return this.http.get<any[]>(url);
  }
}
