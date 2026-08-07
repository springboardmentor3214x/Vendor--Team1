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

  getToken(): string | null {
    return this.getCookie(this.TOKEN_KEY) || sessionStorage.getItem(this.TOKEN_KEY) || localStorage.getItem(this.TOKEN_KEY);
  }

  getUserRole(): string | null {
    return this.getCookie(this.ROLE_KEY) || sessionStorage.getItem(this.ROLE_KEY) || localStorage.getItem(this.ROLE_KEY);
  }

  getCurrentUser(): LoginResponse | null {
    const userStr = this.getCookie(this.USER_KEY) || sessionStorage.getItem(this.USER_KEY) || localStorage.getItem(this.USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  private setCookie(name: string, value: string, days: number = 30): void {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${d.toUTCString()};path=/;SameSite=Lax`;
  }

  private getCookie(name: string): string | null {
    const nameEQ = name + '=';
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i].trim();
      if (c.indexOf(nameEQ) === 0) return decodeURIComponent(c.substring(nameEQ.length));
    }
    return null;
  }

  private deleteCookie(name: string): void {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;SameSite=Lax`;
  }
}
