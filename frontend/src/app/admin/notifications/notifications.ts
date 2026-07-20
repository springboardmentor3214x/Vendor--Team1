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
}

const PLACEHOLDER_NOTIFICATIONS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderNotifications(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_NOTIFICATIONS_ROWS;
}
