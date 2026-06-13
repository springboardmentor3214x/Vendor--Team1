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
}

const PLACEHOLDER_APP_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderApp(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_APP_ROWS;
}
