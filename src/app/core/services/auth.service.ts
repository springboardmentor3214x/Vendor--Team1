import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';

import { LoginRequest } from '../models/login-request';
import { LoginResponse } from '../models/login-response';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly TOKEN_KEY = 'vrip_token';

  private readonly ROLE_KEY = 'vrip_role';

  private readonly USER_KEY = 'vrip_user';

  constructor() {}

  login(request: LoginRequest): Observable<LoginResponse> {

    // -----------------------------
    // Check registered users first
    // -----------------------------

    const users = JSON.parse(
      localStorage.getItem('vrip_registered_users') || '[]'
    );

    const registeredUser = users.find(
      (u: any) =>
        u.email.toLowerCase() === request.email.toLowerCase() &&
        u.password === request.password
    );

    if (registeredUser) {

      const response: LoginResponse = {

        token: 'dummy-jwt-token',

        role: registeredUser.role,

        fullName: registeredUser.fullName,

        email: registeredUser.email

      };

      this.storeSession(response);

      return of(response);

    }

    // -----------------------------
    // Demo Accounts
    // -----------------------------

    let role = 'Vendor';

    switch (request.email.toLowerCase()) {

      case 'admin@vrip.com':
        role = 'Administrator';
        break;

      case 'procurement@vrip.com':
        role = 'Procurement Manager';
        break;

      case 'supply@vrip.com':
        role = 'Supply Chain Manager';
        break;

      case 'finance@vrip.com':
        role = 'Finance Officer';
        break;

      case 'auditor@vrip.com':
        role = 'Auditor';
        break;

      case 'vendor@vrip.com':
        role = 'Vendor';
        break;

      default:
        return throwError(() => new Error('Invalid credentials'));

    }

    const response: LoginResponse = {

      token: 'dummy-jwt-token',

      role,

      fullName: 'Demo User',

      email: request.email

    };

    this.storeSession(response);

    return of(response);

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