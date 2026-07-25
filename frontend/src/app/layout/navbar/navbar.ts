import { Component, OnInit, HostListener, ElementRef } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Search } from '../../ui/search/search';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, Search, RouterModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class Navbar implements OnInit {

  pageTitle: string = '';
  role: string = '';
  fullName: string = '';
  avatarInitial: string = '';
  isMenuOpen: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private elementRef: ElementRef
  ) {}

  ngOnInit(): void {
    this.role = localStorage.getItem('vrip_role') || '';
    this.loadUser();
  }

  toggleMenu(event: Event): void {
    event.stopPropagation();
    this.isMenuOpen = !this.isMenuOpen;
  }

  logout(): void {
    this.authService.logout();
    this.isMenuOpen = false;
    this.router.navigate(['/login']);
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: Event): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.isMenuOpen = false;
    }
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
    if (!this.fullName) {
      this.fullName = this.role || 'User';
    }
    this.avatarInitial = this.fullName.charAt(0).toUpperCase();
  }
}