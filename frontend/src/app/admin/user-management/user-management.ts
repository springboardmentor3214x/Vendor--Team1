import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { UserService } from '../../core/services/user.service';

@Component({
  selector: 'app-user-management',
  standalone: true,
  imports: [CommonModule, Card, Button, Badge],
  templateUrl: './user-management.html',
  styleUrls: ['./user-management.css']
})
export class UserManagement implements OnInit {
  users: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';

  constructor(private userService: UserService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading = true;
    this.errorMsg = '';
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.loading = false;
        if (Array.isArray(data)) {
          this.users = data.map(u => ({
            ...u,
            status: u.account_status || 'Active'
          }));
        } else {
          this.users = [];
        }
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load users', err);
        this.errorMsg = err.error?.detail || err.message || 'Failed to load users from server.';
        this.cdr.markForCheck();
      }
    });
  }

  getInitials(name: string): string {
    if (!name) return 'U';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  }

  getAvatarColorClass(role: string): string {
    switch (role) {
      case 'Administrator': return 'avatar-admin';
      case 'Procurement Manager': return 'avatar-procure';
      case 'Supply Chain Manager': return 'avatar-supply';
      case 'Vendor': return 'avatar-vendor';
      case 'Finance Officer': return 'avatar-finance';
      case 'Auditor': return 'avatar-auditor';
      default: return 'avatar-default';
    }
  }

  approveUser(u: any): void {
    this.userService.approveUser(u.id).subscribe(() => this.loadUsers());
  }

  blockUser(u: any): void {
    this.userService.blockUser(u.id).subscribe(() => this.loadUsers());
  }

  deactivateUser(u: any): void {
    this.userService.deactivateUser(u.id).subscribe(() => this.loadUsers());
  }

  deleteUser(u: any): void {
    if (confirm('Delete ' + u.name + '?')) {
      this.userService.deleteUser(u.id).subscribe(() => this.loadUsers());
    }
  }
}
