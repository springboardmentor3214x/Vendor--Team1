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

  markRead(notificationId: string | number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${notificationId}/read`, {}).pipe(
      tap(() => this.refreshUnreadCount().subscribe())
    );
  }

  markAllRead(): Observable<any> {
    return this.http.put(`${this.apiUrl}/read-all`, {}).pipe(
      tap(() => this.refreshUnreadCount().subscribe())
    );
  }

  triggerBackgroundChecks(): Observable<any> {
    return this.http.post(`${this.apiUrl}/trigger-background-checks`, {});
  }
}
