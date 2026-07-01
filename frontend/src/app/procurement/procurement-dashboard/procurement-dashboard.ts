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
}

const PLACEHOLDER_PROCUREMENT_DASHBOARD_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderProcurementDashboard(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PROCUREMENT_DASHBOARD_ROWS;
}
