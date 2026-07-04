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
}

const PLACEHOLDER_USER_MANAGEMENT_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderUserManagement(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_USER_MANAGEMENT_ROWS;
}
