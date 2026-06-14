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
  register(data: any): Observable<any> {
    return this.http.post(`${this.API_URL}/auth/register`, data);
  }
  forgotPassword(email: string): Observable<any> {
    return this.http.post(`${this.API_URL}/auth/forgot-password`, { email });
  }
  resetPassword(token: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.API_URL}/auth/reset-password`, {
      token, new_password: newPassword
    });
  }
  private mapRole(backendRole: string): string {
    const roleMap: Record<string, string> = {
      'Administrator': 'Administrator',
      'Procurement Manager': 'Procurement Manager',
      'Supply Chain Manager': 'Supply Chain Manager',
      'Vendor': 'Vendor',
      'Finance Officer': 'Finance Officer',
      'Auditor': 'Auditor'
    };
    return roleMap[backendRole] || backendRole;
  }
  private storeSession(response: LoginResponse, rememberMe: boolean): void {
    this.logout();

    if (rememberMe) {
      this.setCookie(this.TOKEN_KEY, response.token, 30);
      this.setCookie(this.ROLE_KEY, response.role, 30);
      this.setCookie(this.USER_KEY, JSON.stringify(response), 30);
    } else {
      sessionStorage.setItem(this.TOKEN_KEY, response.token);
      sessionStorage.setItem(this.ROLE_KEY, response.role);
      sessionStorage.setItem(this.USER_KEY, JSON.stringify(response));
    }
  }
  logout(): void {
    this.deleteCookie(this.TOKEN_KEY);
    this.deleteCookie(this.ROLE_KEY);
    this.deleteCookie(this.USER_KEY);

    sessionStorage.removeItem(this.TOKEN_KEY);
    sessionStorage.removeItem(this.ROLE_KEY);
    sessionStorage.removeItem(this.USER_KEY);

    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.ROLE_KEY);
    localStorage.removeItem(this.USER_KEY);
  }
}

const PLACEHOLDER_AUTH_SERVICE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderAuthService(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_AUTH_SERVICE_ROWS;
  }
  return rows.filter((row) => !!row);
}
