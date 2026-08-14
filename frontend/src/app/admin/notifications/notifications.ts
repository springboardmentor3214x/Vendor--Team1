import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { NotificationService } from '../../core/services/notification.service';
import { CommunicationService } from '../../core/services/communication.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, Badge],
  templateUrl: './notifications.html',
  styleUrls: ['./notifications.css']
})
export class Notifications implements OnInit {
  activeTab: 'notifications' | 'direct_messaging' = 'notifications';

  isLoading = true;
  allNotifications: any[] = [];
  filteredNotifications: any[] = [];
  activeFilter = 'All';
  unreadOnly = false;
  isChecking = false;
  filters = ['All', 'Unread', 'Delivery', 'Contracts', 'System', 'Procurement'];

  registeredUsers: any[] = [];
  selectedUser: any | null = null;
  conversationMessages: any[] = [];
  messageText: string = '';
  selectedFile: File | null = null;
  loadingUsers: boolean = false;
  loadingChat: boolean = false;
  sendingMessage: boolean = false;
  currentUser: any = null;

  selectedRoleFilter: string = 'All Roles';
  roles: string[] = [
    'All Roles',
    'Administrator',
    'Procurement Manager',
    'Supply Chain Manager',
    'Vendor',
    'Finance Officer',
    'Auditor'
  ];

  constructor(
    private notifService: NotificationService,
    private commService: CommunicationService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUser();
    this.loadNotifications();
    this.loadRegisteredUsers();
  }

  get canRunBackgroundChecks(): boolean {
    return this.authService.getUserRole() === 'Administrator';
  }

  get filteredRegisteredUsers(): any[] {
    if (!this.selectedRoleFilter || this.selectedRoleFilter === 'All Roles') {
      return this.registeredUsers;
    }
    return this.registeredUsers.filter(u => u.role?.toLowerCase() === this.selectedRoleFilter.toLowerCase());
  }

  onRoleFilterChange(): void {
    const available = this.filteredRegisteredUsers;
    if (available.length > 0) {
      if (!this.selectedUser || !available.some(u => u.id === this.selectedUser.id)) {
        this.selectUser(available[0]);
      }
    } else {
      this.selectedUser = null;
      this.conversationMessages = [];
    }
  }

  loadNotifications(): void {
    this.isLoading = true;
    this.notifService.getNotifications().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.length > 0) {
          this.allNotifications = res.map((n: any) => ({
            id: n.id,
            title: n.title,
            message: n.description,
            module: n.module_name || 'System',
            priority: n.priority || 'Medium',
            time: n.timestamp ? new Date(n.timestamp).toLocaleString() : 'Recently',
            type: n.priority === 'High' || n.priority === 'Critical' ? 'alert' : (n.priority === 'Low' ? 'info' : 'warning'),
            icon: n.priority === 'High' ? 'error' : (n.module_name === 'Delivery' ? 'local_shipping' : (n.module_name === 'Contracts' ? 'description' : 'notifications')),
            unread: !n.is_read
          }));
        } else {
          this.allNotifications = [];
        }
        this.applyFilter();
      },
      error: () => {
        this.isLoading = false;
        this.allNotifications = [];
        this.applyFilter();
      }
    });
  }

  setFilter(filter: string): void {
    this.activeFilter = filter;
    this.unreadOnly = filter === 'Unread';
    this.applyFilter();
  }

  applyFilter(): void {
    if (this.activeFilter === 'All') {
      this.filteredNotifications = [...this.allNotifications];
    } else if (this.activeFilter === 'Unread') {
      this.filteredNotifications = this.allNotifications.filter(n => n.unread);
    } else {
      this.filteredNotifications = this.allNotifications.filter(n => n.module.toLowerCase() === this.activeFilter.toLowerCase());
    }
  }

  markRead(notif: any): void {
    if (!notif.unread) return;
    this.notifService.markRead(notif.id).subscribe({
      next: () => {
        notif.unread = false;
      }
    });
  }

  markAllRead(): void {
    this.notifService.markAllRead().subscribe({
      next: () => {
        this.allNotifications.forEach(n => n.unread = false);
        this.applyFilter();
      }
    });
  }

  triggerChecks(): void {
    this.isChecking = true;
    this.notifService.triggerBackgroundChecks().subscribe({
      next: () => {
        this.isChecking = false;
        this.loadNotifications();
      },
      error: () => {
        this.isChecking = false;
      }
    });
  }

  loadRegisteredUsers(): void {
    this.loadingUsers = true;
    this.commService.getRegisteredRecipients().subscribe({
      next: (users) => {
        this.loadingUsers = false;
        this.registeredUsers = users || [];
        const available = this.filteredRegisteredUsers;
        if (available.length > 0 && !this.selectedUser) {
          this.selectUser(available[0]);
        }
      },
      error: (err) => {
        this.loadingUsers = false;
        console.error('Failed to load registered recipients', err);
      }
    });
  }

  selectUser(user: any): void {
    this.selectedUser = user;
    this.loadConversationWithUser(user);
  }

  loadConversationWithUser(user: any): void {
    if (!user) return;
    this.loadingChat = true;
    this.commService.getMessages(undefined, undefined, undefined, undefined, user.id).subscribe({
      next: (msgs) => {
        this.loadingChat = false;
        if (Array.isArray(msgs)) {
          this.conversationMessages = msgs;
        } else {
          this.conversationMessages = [];
        }
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.loadingChat = false;
        console.error('Failed to load conversation messages', err);
        this.conversationMessages = [];
        this.cdr.markForCheck();
      }
    });
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }

  sendDirectMessage(): void {
    if (!this.messageText.trim() && !this.selectedFile) return;
    if (!this.selectedUser) {
      alert('Please select a registered recipient first.');
      return;
    }

    this.sendingMessage = true;

    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('message', this.messageText.trim() || 'Sent attachment');
      formData.append('receiver_id', String(this.selectedUser.id));
      formData.append('receiver_name', this.selectedUser.name);
      formData.append('file', this.selectedFile, this.selectedFile.name);

      this.commService.sendMessageWithFile(formData).subscribe({
        next: () => {
          this.sendingMessage = false;
          this.messageText = '';
          this.selectedFile = null;
          this.loadConversationWithUser(this.selectedUser);
        },
        error: (err: any) => {
          this.sendingMessage = false;
          alert('Failed to send message: ' + (err.error?.detail || err.message));
        }
      });
    } else {
      const payload = {
        receiver_id: this.selectedUser.id,
        receiver_name: this.selectedUser.name,
        message: this.messageText.trim()
      };

      this.commService.sendMessage(payload).subscribe({
        next: () => {
          this.sendingMessage = false;
          this.messageText = '';
          this.loadConversationWithUser(this.selectedUser);
        },
        error: (err: any) => {
          this.sendingMessage = false;
          alert('Failed to send message: ' + (err.error?.detail || err.message));
        }
      });
    }
  }

  getDownloadUrl(msg: any): string {
    if (msg.file_path) {
      return '/' + msg.file_path.replace(/\\/g, '/');
    }
    return `/static/communications/${msg.file_name || ''}`;
  }

  getBadgeVariant(priority: string): 'danger' | 'warning' | 'info' | 'default' {
    if (priority === 'High' || priority === 'Critical') return 'danger';
    if (priority === 'Medium') return 'warning';
    if (priority === 'Low') return 'info';
    return 'default';
  }
}