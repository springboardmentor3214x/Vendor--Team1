import { Component, OnInit } from '@angular/core';
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

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data.map(u => ({
          ...u,
          status: u.account_status || 'Active'
        }));
      },
      error: (err) => {
        console.error('Failed to load users', err);
      }
    });
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
