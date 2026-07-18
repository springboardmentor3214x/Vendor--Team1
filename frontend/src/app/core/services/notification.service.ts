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
}

const PLACEHOLDER_NOTIFICATION_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderNotificationService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_NOTIFICATION_SERVICE_ROWS;
}
