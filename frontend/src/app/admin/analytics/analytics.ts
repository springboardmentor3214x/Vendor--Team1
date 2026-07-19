import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { NgApexchartsModule } from 'ng-apexcharts';
import { AnalyticsService } from '../../core/services/analytics.service';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, Card, Button, NgApexchartsModule],
  templateUrl: './analytics.html',
  styleUrls: ['./analytics.css']
})
export class Analytics implements OnInit {
  isLoading = true;
  totalUsers = 0;
  activeUsers = 0;
  totalRoles = 6;
  totalVendors = 0;
  totalContracts = 0;
}

const PLACEHOLDER_ANALYTICS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderAnalytics(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_ANALYTICS_ROWS;
}
