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
}

const PLACEHOLDER_NOTIFICATIONS_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 6, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 7, name: 'Northwind Steel', status: 'Active' },
  { id: 8, name: 'Orbit IT Systems', status: 'Pending Approval' },
];

function usePlaceholderNotifications(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_NOTIFICATIONS_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
