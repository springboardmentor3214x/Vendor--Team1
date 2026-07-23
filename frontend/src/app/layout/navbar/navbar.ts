import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Search } from '../../ui/search/search';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [Search, RouterModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class Navbar implements OnInit {

  pageTitle: string = '';
  role: string = '';
  fullName: string = '';
  avatarInitial: string = '';

  ngOnInit(): void {
    this.role = localStorage.getItem('vrip_role') || '';
    this.loadUser();
  }

  private loadUser(): void {
    const stored = localStorage.getItem('vrip_user');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        this.fullName = parsed.fullName || parsed.name || '';
        this.role = parsed.role || this.role;
      } catch {
        this.fullName = '';
      }
    }
    // Use role key as fallback display name
    if (!this.fullName) {
      this.fullName = this.role || 'User';
    }
    this.avatarInitial = this.fullName.charAt(0).toUpperCase();
  }
}