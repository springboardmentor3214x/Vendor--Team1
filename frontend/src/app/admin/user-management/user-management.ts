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

  closeEditModal(): void {
    this.showEditModal = false;
    this.editUser = null;
  }

  submitEdit(): void {
    if (!this.editUser) return;
    this.formError = '';
    if (!this.editUser.name.trim()) {
      this.formError = 'Name cannot be empty.';
      return;
    }
    this.savingUser = true;
    const payload: any = {
      name: this.editUser.name,
      mobile_number: this.editUser.mobile_number,
      role: this.editUser.role
    };
    this.userService.updateUser(this.editUser.id, payload).subscribe({
      next: () => {
        this.savingUser = false;
        this.showEditModal = false;
        this.editUser = null;
        this.loadUsers();
      },
      error: (err) => {
        this.savingUser = false;
        this.formError = err.error?.detail || 'Failed to update user.';
      }
    });
  }

  openResetModal(u: any): void {
    this.resetUser = u;
    this.resetPasswordValue = '';
    this.formError = '';
    this.showResetModal = true;
  }

  closeResetModal(): void {
    this.showResetModal = false;
    this.resetUser = null;
  }

  submitReset(): void {
    if (!this.resetUser) return;
    this.formError = '';
    if (this.resetPasswordValue.length < 8) {
      this.formError = 'Password must be at least 8 characters.';
      return;
    }
    this.savingUser = true;
    this.userService.resetPassword(this.resetUser.id, this.resetPasswordValue).subscribe({
      next: () => {
        this.savingUser = false;
        this.showResetModal = false;
        alert(`Password reset for ${this.resetUser.name}.`);
        this.resetUser = null;
      },
      error: (err) => {
        this.savingUser = false;
        this.formError = err.error?.detail || 'Failed to reset password.';
      }
    });
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

  openMessageModal(u: any): void {
    this.selectedUserForMessage = u;
    this.messageText = '';
    this.showMessageModal = true;
  }

  closeMessageModal(): void {
    this.showMessageModal = false;
    this.selectedUserForMessage = null;
  }

  sendDirectMessage(): void {
    if (!this.selectedUserForMessage || !this.messageText.trim()) return;

    this.sendingMessage = true;
    const payload = {
      receiver_id: this.selectedUserForMessage.id,
      receiver_name: this.selectedUserForMessage.name,
      message: this.messageText.trim()
    };

    this.commService.sendMessage(payload).subscribe({
      next: () => {
        this.sendingMessage = false;
        alert(`Message sent to ${this.selectedUserForMessage.name}!`);
        this.closeMessageModal();
      },
      error: (err) => {
        this.sendingMessage = false;
        alert('Failed to send message: ' + (err.error?.detail || err.message));
      }
    });
  }
}
