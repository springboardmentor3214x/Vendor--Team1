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
    this.role = this.authService.getUserRole() || '';
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
    const user = this.authService.getCurrentUser();
    if (user) {
      this.fullName = user.fullName || user.email || '';
      this.role = user.role || this.role;
    }
    if (!this.fullName) {
      this.fullName = this.role || 'User';
    }
    this.avatarInitial = this.fullName.charAt(0).toUpperCase();
  }
}