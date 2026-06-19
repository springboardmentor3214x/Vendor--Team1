import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { Sidebar } from './layout/sidebar/sidebar';
import { Navbar } from './layout/navbar/navbar';

const AUTH_ROUTES = ['/login', '/register', '/forgot-password', '/reset-password'];

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    Sidebar,
    Navbar,
    RouterOutlet
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  constructor(public router: Router) {}

  get showShell(): boolean {
    const path = this.router.url.split(/[?#]/)[0];
    return !AUTH_ROUTES.includes(path);
  }

}
