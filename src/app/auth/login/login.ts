import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule,
    RouterModule
  ],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  email: string = '';

  password: string = '';

  rememberMe: boolean = false;

  showPassword: boolean = false;

  constructor(private router: Router) {}

  togglePassword() {

    this.showPassword = !this.showPassword;

  }

  login() {

    // Backend JWT authentication will be connected later

    this.router.navigate(['/dashboard']);

  }

}