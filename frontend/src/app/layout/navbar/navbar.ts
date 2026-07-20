import { Component } from '@angular/core';
import { Search } from '../../ui/search/search';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [Search],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class Navbar {
  pageTitle: string = '';
  role: string = '';

  constructor() {
    this.role = localStorage.getItem('vrip_role') || '';
  }
}