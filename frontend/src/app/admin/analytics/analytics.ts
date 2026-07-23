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
  totalProcurements = 0;
  complianceRate = 100;
  totalSpend = '₹0.00';
  public categorySpendChart: any;
  public orderStatusChart: any;
}

const PLACEHOLDER_ANALYTICS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderAnalytics(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_ANALYTICS_ROWS;
  }
  return rows.filter((row) => !!row);
}
