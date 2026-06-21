import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button],
  templateUrl: './settings.html',
  styleUrls: ['./settings.css']
})
export class Settings implements OnInit {
  activeTab: 'general' | 'security' | 'notifications' = 'general';
  successMessage = '';
  errorMessage = '';
  isSubmitting = false;
  language = 'English (US)';
  timezone = '(GMT+05:30) India Standard Time';
  dateFormat = 'DD/MM/YYYY';
  currency = 'INR (₹)';
  currentPassword = '';
  newPassword = '';
  confirmPassword = '';
}

const PLACEHOLDER_SETTINGS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderSettings(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_SETTINGS_ROWS;
}
