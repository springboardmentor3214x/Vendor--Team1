import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators,
  FormGroup
} from '@angular/forms';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';

import { AuthService } from '../../core/services/auth.service';
import { ThemeService } from '../../core/services/theme.service';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule
  ],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {

  hidePassword = true;

  loading = false;

  errorMessage = '';

  loginForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    public themeService: ThemeService
  ) {

    this.loginForm = this.fb.group({

      email: [
        '',
        [
          Validators.required,
          Validators.email
        ]
      ],

      password: [
        '',
        [
          Validators.required
        ]
      ],

      rememberMe: [false]

    });

  }

  togglePassword(): void {

    this.hidePassword = !this.hidePassword;

  }

  fieldError(controlName: 'email' | 'password'): string {

    const control = this.loginForm.get(controlName);

    if (!control || control.valid || !(control.touched || control.dirty)) {
      return '';
    }

    if (control.hasError('required')) {
      return controlName === 'email'
        ? 'Email address is required'
        : 'Password cannot be empty';
    }

    if (control.hasError('email')) {
      return 'Enter a valid email address';
    }

    return '';

  }

  login(): void {

    this.errorMessage = '';

    if (this.loginForm.invalid) {

      this.loginForm.markAllAsTouched();

      return;

    }

    this.loading = true;

    this.authService.login({

      email: this.loginForm.value.email,

      password: this.loginForm.value.password,

      rememberMe: this.loginForm.value.rememberMe

    }).subscribe({

      next: () => {

        this.loading = false;

        const returnUrl = this.route.snapshot.queryParamMap.get('returnUrl');
        if (returnUrl) {
          this.router.navigateByUrl(returnUrl);
          return;
        }

        const role = this.authService.getUserRole();

        switch (role) {

          case 'Administrator':
            this.router.navigate(['/admin-dashboard']);
            break;

          case 'Procurement Manager':
            this.router.navigate(['/procurement-dashboard']);
            break;

          case 'Supply Chain Manager':
            this.router.navigate(['/supply-chain-dashboard']);
            break;

          case 'Vendor':
            this.router.navigate(['/vendor-dashboard']);
            break;

          case 'Finance Officer':
            this.router.navigate(['/finance-dashboard']);
            break;

          case 'Auditor':
            this.router.navigate(['/auditor-dashboard']);
            break;

          default:
            this.router.navigate(['/login']);

        }

      },

      error: (err) => {
        this.loading = false;
        this.errorMessage = err.message || err.error?.detail || 'Invalid email or password';
      }

    });

  }

}