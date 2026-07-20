import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { CommonModule } from '@angular/common';

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

  newPassword = '';

  confirmPassword = '';

  hidePassword = true;

  hideConfirmPassword = true;

  loading = false;

  passwordReset = false;

  constructor(private router: Router) {}

  resetPassword() {

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

    this.loading = true;

    // Backend API will be connected here later

    setTimeout(() => {

      this.loading = false;

      this.passwordReset = true;

    }, 1000);

  }

}