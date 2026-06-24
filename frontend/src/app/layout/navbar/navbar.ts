import { Component, OnInit, OnDestroy, HostListener, ElementRef, ChangeDetectorRef } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { Search } from '../../ui/search/search';
import { AuthService } from '../../core/services/auth.service';
import { NotificationService } from '../../core/services/notification.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, Search, RouterModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export class Navbar implements OnInit, OnDestroy {

  pageTitle: string = '';
  role: string = '';
  fullName: string = '';
  avatarInitial: string = '';
  isMenuOpen: boolean = false;
  unreadCount = 0;

  private unreadSub?: Subscription;
  private pollHandle?: ReturnType<typeof setInterval>;

  constructor(
    private authService: AuthService,
    private router: Router,
    private elementRef: ElementRef,
    private notificationService: NotificationService,
    private cdr: ChangeDetectorRef
  ) {}

  get notificationsRoute(): string {
    return this.role === 'Administrator' ? '/admin/notifications' : '/notification-center';
  }

  ngOnInit(): void {
    this.role = this.authService.getUserRole() || '';
    this.loadUser();

    this.unreadSub = this.notificationService.unreadCount$.subscribe(count => {
      this.unreadCount = count;
      this.cdr.markForCheck();
    });
    this.notificationService.refreshUnreadCount().subscribe();

    this.pollHandle = setInterval(
      () => this.notificationService.refreshUnreadCount().subscribe(),
      60000
    );
  }

  ngOnDestroy(): void {
    this.unreadSub?.unsubscribe();
    if (this.pollHandle) {
      clearInterval(this.pollHandle);
    }
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