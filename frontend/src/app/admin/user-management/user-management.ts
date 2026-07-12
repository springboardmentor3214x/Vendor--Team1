import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { UserService } from '../../core/services/user.service';
import { CommunicationService } from '../../core/services/communication.service';
import { AuthService } from '../../core/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-management',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, Badge],
  templateUrl: './user-management.html',
  styleUrls: ['./user-management.css']
})
export class UserManagement implements OnInit {
  users: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';
  showMessageModal: boolean = false;
  selectedUserForMessage: any | null = null;
  messageText: string = '';
  sendingMessage: boolean = false;
  readonly roles: string[] = [
    'Administrator', 'Procurement Manager', 'Supply Chain Manager',
    'Vendor', 'Finance Officer', 'Auditor'
  ];
  currentEmail: string = '';
  showRegisterModal = false;
  savingUser = false;
  formError = '';
  newUser: any = { name: '', email: '', mobile_number: '', role: 'Procurement Manager', company_name: '', password: '' };
  showEditModal = false;
  editUser: any = null;
  showResetModal = false;
  resetUser: any = null;
  resetPasswordValue = '';
  constructor(
    private userService: UserService,
    private commService: CommunicationService,
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}
  ngOnInit(): void {
    this.currentEmail = (this.authService.getCurrentUser()?.email || '').toLowerCase();
    this.loadUsers();
  }
  isSelf(u: any): boolean {
    return !!u && (u.email || '').toLowerCase() === this.currentEmail;
  }
  openRegisterModal(): void {
    this.newUser = { name: '', email: '', mobile_number: '', role: 'Procurement Manager', company_name: '', password: '' };
    this.formError = '';
    this.showRegisterModal = true;
  }
  closeRegisterModal(): void {
    this.showRegisterModal = false;
  }
  submitRegister(): void {
    this.formError = '';
    if (!this.newUser.name.trim() || !this.newUser.email.trim() || !this.newUser.password) {
      this.formError = 'Name, email and password are required.';
      return;
    }
    if (this.newUser.password.length < 8) {
      this.formError = 'Password must be at least 8 characters.';
      return;
    }
    if (this.newUser.role === 'Vendor' && !this.newUser.company_name.trim()) {
      this.formError = 'Company name is required for the Vendor role.';
      return;
    }
    this.savingUser = true;
    this.userService.createUser(this.newUser).subscribe({
      next: () => {
        this.savingUser = false;
        this.showRegisterModal = false;
        this.loadUsers();
      },
      error: (err) => {
        this.savingUser = false;
        this.formError = err.error?.detail || 'Failed to create user.';
      }
    });
  }
  openEditModal(u: any): void {
    this.editUser = { id: u.id, name: u.name, mobile_number: u.mobile_number || '', role: u.role, email: u.email };
    this.formError = '';
    this.showEditModal = true;
  }
}

const PLACEHOLDER_USER_MANAGEMENT_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderUserManagement(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_USER_MANAGEMENT_ROWS;
  }
  return rows.filter((row) => !!row);
}
