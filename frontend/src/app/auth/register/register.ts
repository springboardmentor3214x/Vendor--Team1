import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    FormsModule,
    RouterModule
  ],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register {

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

    if (!this.user.fullName.trim()) {

      alert('Full Name is required');

      return;

    }

    if (!this.user.email.trim()) {

      alert('Email is required');

      return;

    }

    if (!this.user.password) {

      alert('Password is required');

      return;

    }

    if (this.user.password !== this.user.confirmPassword) {

      alert('Passwords do not match');

      return;

    }

    alert('Registration Successful');

    this.router.navigate(['/login']);

  }

}