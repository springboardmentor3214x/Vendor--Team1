import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { silentRequest } from '../interceptors/http-context';

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private apiUrl = '/notifications';
  private unreadCountSubject = new BehaviorSubject<number>(0);
  readonly unreadCount$ = this.unreadCountSubject.asObservable();
  constructor(private http: HttpClient) {}
  refreshUnreadCount(): Observable<number> {

    return this.http.get<{ unread_count: number }>(`${this.apiUrl}/unread-count`, {
      context: silentRequest()
    }).pipe(
      map(res => res?.unread_count ?? 0),
      tap(count => this.unreadCountSubject.next(count)),
      catchError(() => of(this.unreadCountSubject.value))
    );
  }
  createNotification(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data);
  }
  getNotifications(moduleName?: string, priority?: string, unreadOnly: boolean = false, limit: number = 100): Observable<any[]> {
    let query = [`unread_only=${unreadOnly}`, `limit=${limit}`];
    if (moduleName && moduleName !== 'All') query.push(`module=${moduleName}`);
    if (priority && priority !== 'All') query.push(`priority=${priority}`);

    return this.http.get<any[]>(`${this.apiUrl}/?${query.join('&')}`);
  }
}

const PLACEHOLDER_NOTIFICATION_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderNotificationService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_NOTIFICATION_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
