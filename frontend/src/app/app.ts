import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { Sidebar } from './layout/sidebar/sidebar';
import { Navbar } from './layout/navbar/navbar';

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