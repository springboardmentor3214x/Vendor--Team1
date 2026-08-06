import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private apiUrl = '/notifications';

  constructor(private http: HttpClient) {}

  createNotification(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data);
  }

  getNotifications(moduleName?: string, priority?: string, unreadOnly: boolean = false, limit: number = 100): Observable<any[]> {
    let query = [`unread_only=${unreadOnly}`, `limit=${limit}`];
    if (moduleName && moduleName !== 'All') query.push(`module=${moduleName}`);
    if (priority && priority !== 'All') query.push(`priority=${priority}`);

    return this.http.get<any[]>(`${this.apiUrl}/?${query.join('&')}`);
  }

  markRead(notificationId: string | number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${notificationId}/read`, {});
  }

  markAllRead(): Observable<any> {
    return this.http.put(`${this.apiUrl}/read-all`, {});
  }

  triggerBackgroundChecks(): Observable<any> {
    return this.http.post(`${this.apiUrl}/trigger-background-checks`, {});
  }
}
