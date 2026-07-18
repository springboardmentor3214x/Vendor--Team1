import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register {
  loading = false;
  
  user = {

    fullName: '',

    employeeId: '',

    companyName: '',

    email: '',

    mobile: '',

    password: '',

    confirmPassword: '',

    role: 'Vendor'

  };

  constructor(private router: Router) {}

  get isVendor(): boolean {

    return this.user.role === 'Vendor';

  }

  register() {

    // Full Name

    if (!this.user.fullName.trim()) {

      alert('Full Name is required');

      return;

    }

    // Employee ID / Company Name

    if (this.isVendor) {

      if (!this.user.companyName.trim()) {

        alert('Company Name is required');

        return;

      }

    } else {

      if (!this.user.employeeId.trim()) {

        alert('Employee ID is required');

        return;

      }

    }

    // Email

    if (!this.user.email.trim()) {

      alert('Email is required');

      return;

    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(this.user.email)) {

      alert('Enter a valid email address');

      return;

    }

    // Mobile Number

    if (!/^[0-9]{10}$/.test(this.user.mobile)) {

      alert('Enter a valid 10-digit mobile number');

      return;

    }

    // Password

    if (!this.user.password) {

      alert('Password is required');

      return;

    }

    if (this.user.password.length < 8) {

      alert('Password must be at least 8 characters');

      return;

    }

    // Confirm Password

    if (!this.user.confirmPassword) {

      alert('Confirm Password is required');

      return;

    }

    if (this.user.password !== this.user.confirmPassword) {

      alert('Passwords do not match');

      return;

    }

    // Check duplicate email

    const users = JSON.parse(

      localStorage.getItem('vrip_registered_users') || '[]'

    );

    const emailExists = users.some(

      (u: any) => u.email.toLowerCase() === this.user.email.toLowerCase()

    );

    if (emailExists) {

      alert('Email already registered');

      return;

    }

    // Save user

    users.push({

      fullName: this.user.fullName,

      email: this.user.email,

      password: this.user.password,

      role: this.user.role

    });

    localStorage.setItem(

      'vrip_registered_users',

      JSON.stringify(users)

    );

    alert('Registration Successful');

    this.router.navigate(['/login']);

  }

}