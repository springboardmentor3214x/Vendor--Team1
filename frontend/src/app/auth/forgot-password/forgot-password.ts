import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './forgot-password.html',
  styleUrls: ['./forgot-password.css']
})
export class ForgotPassword {
  email = '';
  loading = false;
  emailSent = false;
  errorMessage = '';

  emailDelivered = false;
  resetToken = '';
  expiresInMinutes = 0;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  goToReset(): void {
    this.router.navigate(['/reset-password'], {
      queryParams: { token: this.resetToken }
    });
  }

  sendResetLink() {
    this.errorMessage = '';
    if (!this.email.trim()) {
      alert('Email is required');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.email)) {
      alert('Enter a valid email address');
      return;
    }

    this.loading = true;
    this.authService.forgotPassword(this.email.trim()).subscribe({
      next: (res: any) => {
        this.loading = false;
        this.emailSent = true;
        this.emailDelivered = !!res?.email_delivered;
        this.resetToken = res?.reset_token || '';
        this.expiresInMinutes = res?.expires_in_minutes || 15;
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || err.message || 'Failed to send reset link';
      }
    });
  }
}