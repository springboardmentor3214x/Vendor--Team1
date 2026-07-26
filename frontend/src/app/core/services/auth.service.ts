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
          email: res.user.email
        };
        this.storeSession(response);
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

  private storeSession(response: LoginResponse): void {
    localStorage.setItem(this.TOKEN_KEY, response.token);
    localStorage.setItem(this.ROLE_KEY, response.role);
    localStorage.setItem(this.USER_KEY, JSON.stringify(response));
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.ROLE_KEY);
    localStorage.removeItem(this.USER_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getUserRole(): string | null {
    return localStorage.getItem(this.ROLE_KEY);
  }

  getCurrentUser(): LoginResponse | null {
    const user = localStorage.getItem(this.USER_KEY);
    return user ? JSON.parse(user) : null;
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
