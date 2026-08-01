import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ThemeService } from '../../core/services/theme.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule
  ],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register implements OnInit {
  loading = false;
  
  constructor(
    private router: Router,
    public themeService: ThemeService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    try {
      localStorage.removeItem('vrip_registered_users');
    } catch (e) {
      // Ignore storage errors
    }
  }

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

  get isVendor(): boolean {
    return this.user.role === 'Vendor';
  }

  register() {
    if (!this.user.fullName.trim()) {
      alert('Full Name is required');
      return;
    }

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

    if (!this.user.email.trim()) {
      alert('Email is required');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.user.email)) {
      alert('Enter a valid email address');
      return;
    }

    if (!/^[0-9]{10}$/.test(this.user.mobile)) {
      alert('Enter a valid 10-digit mobile number');
      return;
    }

    if (!this.user.password) {
      alert('Password is required');
      return;
    }

    if (this.user.password.length < 8) {
      alert('Password must be at least 8 characters');
      return;
    }

    if (!this.user.confirmPassword) {
      alert('Confirm Password is required');
      return;
    }

    if (this.user.password !== this.user.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    const payload = {
      name: this.user.fullName.trim(),
      email: this.user.email.trim(),
      mobile_number: this.user.mobile.trim(),
      company_name: this.user.companyName.trim(),
      password: this.user.password,
      role: this.user.role
    };

    this.loading = true;
    this.authService.register(payload).subscribe({
      next: () => {
        this.loading = false;
        alert('Registration Successful');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.loading = false;
        alert(err.error?.detail || err.message || 'Registration failed');
      }
    });
  }
}