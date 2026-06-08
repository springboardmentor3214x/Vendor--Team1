import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError, catchError, map } from 'rxjs';
import { LoginRequest } from '../models/login-request';
import { LoginResponse } from '../models/login-response';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly API_URL = '';
  private readonly TOKEN_KEY = 'vrip_token';
  private readonly ROLE_KEY = 'vrip_role';
  private readonly USER_KEY = 'vrip_user';
  constructor(private http: HttpClient) {}
  login(request: LoginRequest): Observable<LoginResponse> {
    return this.http.post<any>(`${this.API_URL}/auth/login`, {
      email: request.email,
      password: request.password
    }).pipe(
      map(res => {
        const response: LoginResponse = {
          token: res.access_token,
          role: this.mapRole(res.user.role),
          fullName: res.user.name,
          email: res.user.email,
          mobileNumber: res.user.mobile_number
        };
        this.storeSession(response, !!request.rememberMe);
        return response;
      }),
      catchError(err => throwError(() => new Error(
        err.error?.detail || 'Invalid email or password'
      )))
    );
  }
}

const PLACEHOLDER_AUTH_SERVICE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderAuthService(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_AUTH_SERVICE_ROWS;
}
