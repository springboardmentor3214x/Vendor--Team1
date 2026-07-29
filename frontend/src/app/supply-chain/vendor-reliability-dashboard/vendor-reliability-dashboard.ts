import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { InputComponent } from '../../ui/input/input';
import { ReliabilityService } from '../../core/services/reliability.service';
import { ReportsService } from '../../core/services/reports.service';

@Component({
  selector: 'app-vendor-reliability-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Card, Button, Table, InputComponent],
  templateUrl: './vendor-reliability-dashboard.html',
  styleUrls: ['./vendor-reliability-dashboard.css']
})
export class VendorReliabilityDashboard implements OnInit {
  isLoading = true;
  errorMsg = '';
  summary = {
    totalVendors: 0,
    averageScore: 0,
    highReliability: 0,
    mediumReliability: 0,
    highRisk: 0
  };
  allVendors: any[] = [];
  vendors: any[] = [];
}

const PLACEHOLDER_VENDOR_RELIABILITY_DASHBOARD_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorReliabilityDashboard(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_RELIABILITY_DASHBOARD_ROWS;
}
