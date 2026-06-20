import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './profile.html',
  styleUrls: ['./profile.css']
})
export class Profile implements OnInit {
  isEditing = false;
  user = {
    fullName: '',
    email: '',
    mobile: '',
    role: '',
    employeeId: ''
  };
  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private router: Router
  ) {}
  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.user.fullName = currentUser.fullName || '';
      this.user.email = currentUser.email || '';
      this.user.mobile = (currentUser as any).mobileNumber || (currentUser as any).mobile || '';
      this.user.role = currentUser.role || this.authService.getUserRole() || '';
    }

    this.http.get<any>('/users/me').subscribe({
      next: (data) => {
        this.user.fullName = data.name || this.user.fullName;
        this.user.email    = data.email || this.user.email;
        this.user.mobile   = data.mobile_number || data.phone || this.user.mobile;
        this.user.role     = data.role || this.user.role;
        this.user.employeeId = data.employee_id || '';
      },
      error: () => {}
    });
  }
  set fullName(val: string) {
    this.user.fullName = val;
  }
}

const PLACEHOLDER_PROFILE_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderProfile(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PROFILE_ROWS;
  }
  return rows.filter((row) => !!row);
}
