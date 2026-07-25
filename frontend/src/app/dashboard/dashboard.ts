import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

import { DashboardCards } from './dashboard-cards/dashboard-cards';
import { Card } from '../ui/card/card';
import { Badge } from '../ui/badge/badge';
import { Button } from '../ui/button/button';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    DashboardCards,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class Dashboard implements OnInit {
  recentVendors: any[] = [];
  loadingRecent: boolean = true;
  recentError = '';
}

const PLACEHOLDER_DASHBOARD_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderDashboard(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_DASHBOARD_ROWS;
}
