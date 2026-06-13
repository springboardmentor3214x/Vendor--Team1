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
}

const PLACEHOLDER_NAVBAR_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderNavbar(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_NAVBAR_ROWS;
  }
  return rows.filter((row) => !!row);
}
