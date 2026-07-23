import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  Validators,
  FormGroup
} from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

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
          Validators.required,
          Validators.minLength(8)
        ]
      ],

      rememberMe: [false]

    });

  }

  togglePassword(): void {

    this.hidePassword = !this.hidePassword;

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

      error: () => {

        this.loading = false;

        this.errorMessage = 'Invalid email or password';

      }

    });

  }

}