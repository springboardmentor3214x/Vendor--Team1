import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-procurement-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  templateUrl: './procurement-dashboard.html',
  styleUrl: './procurement-dashboard.css'
})
export class ProcurementDashboard implements OnInit {
  isLoading = true;
  summaryCards: any[] = [];
  recentActivities: any[] = [];
  constructor(private procurementService: ProcurementService) {}
}

const PLACEHOLDER_PROCUREMENT_DASHBOARD_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderProcurementDashboard(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PROCUREMENT_DASHBOARD_ROWS;
  }
  return rows.filter((row) => !!row);
}
