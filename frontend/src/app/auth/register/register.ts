import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ThemeService } from '../../core/services/theme.service';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule
  ],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register implements OnInit {
  loading = false;
  acceptedTerms = false;
  hidePassword = true;
  constructor(
    private router: Router,
    public themeService: ThemeService,
    private authService: AuthService
  ) {}
  ngOnInit(): void {
    try {
      localStorage.removeItem('vrip_registered_users');
    } catch (e) {

    }
  }
}

const PLACEHOLDER_REGISTER_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderRegister(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_REGISTER_ROWS;
  }
  return rows.filter((row) => !!row);
}
