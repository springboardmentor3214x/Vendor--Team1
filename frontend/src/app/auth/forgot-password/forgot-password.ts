import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { CommonModule } from '@angular/common';

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

  constructor(private router: Router) {}

  sendResetLink() {

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

    // Backend API will be connected here later

    setTimeout(() => {

      this.loading = false;

      this.emailSent = true;

    }, 1000);

  }

}