import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './reset-password.html',
  styleUrls: ['./reset-password.css']
})
export class ResetPassword {

  token = '';
  newPassword = '';
  confirmPassword = '';
  hidePassword = true;
  hideConfirmPassword = true;
  loading = false;
  passwordReset = false;
  errorMessage = '';

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private authService: AuthService
  ) {
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
  }

  resetPassword() {
    this.errorMessage = '';
    if (!this.newPassword) {
      alert('New Password is required');
      return;
    }

    if (this.newPassword.length < 8) {
      alert('Password must be at least 8 characters');
      return;
    }

    if (!this.confirmPassword) {
      alert('Confirm Password is required');
      return;
    }

    if (this.newPassword !== this.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    if (!this.token) {
      alert('Missing reset token. Please check your reset link.');
      return;
    }

    this.loading = true;
    this.authService.resetPassword(this.token, this.newPassword).subscribe({
      next: () => {
        this.loading = false;
        this.passwordReset = true;
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.detail || err.message || 'Failed to reset password';
      }
    });
  }
}