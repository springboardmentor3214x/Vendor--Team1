import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CommunicationService {
  private apiUrl = '/communication';

  constructor(private http: HttpClient) {}

  sendMessage(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/messages`, data);
  }

  sendMessageWithFile(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/messages/upload`, formData);
  }

  getMessages(vendorId?: number, poId?: number, contractId?: number, discussionId?: number): Observable<any[]> {
    let query = [];
    if (vendorId) query.push(`vendor_id=${vendorId}`);
    if (poId) query.push(`po_id=${poId}`);
    if (contractId) query.push(`contract_id=${contractId}`);
    if (discussionId) query.push(`discussion_id=${discussionId}`);

    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any[]>(`${this.apiUrl}/messages${queryString}`);
  }

  createDiscussion(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/discussions`, data);
  }

  getDiscussions(vendorId?: number, poId?: number): Observable<any[]> {
    let query = [];
    if (vendorId) query.push(`vendor_id=${vendorId}`);
    if (poId) query.push(`po_id=${poId}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any[]>(`${this.apiUrl}/discussions${queryString}`);
  }

  uploadFile(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/files/upload`, formData);
  }

  getFiles(vendorId?: number, poId?: number, contractId?: number): Observable<any[]> {
    let query = [];
    if (vendorId) query.push(`vendor_id=${vendorId}`);
    if (poId) query.push(`po_id=${poId}`);
    if (contractId) query.push(`contract_id=${contractId}`);
    const queryString = query.length ? `?${query.join('&')}` : '';
    return this.http.get<any[]>(`${this.apiUrl}/files${queryString}`);
  }

  getActivityLogs(moduleName?: string, limit: number = 100): Observable<any[]> {
    let url = `${this.apiUrl}/activity-logs?limit=${limit}`;
    if (moduleName && moduleName !== 'All') {
      url += `&module=${moduleName}`;
    }
    return this.http.get<any[]>(url);
  }
}
