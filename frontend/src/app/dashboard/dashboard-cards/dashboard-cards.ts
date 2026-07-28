import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface VendorStats {
  total: number;
  approved: number;
  pending_review: number;
  suspended: number;
  rejected: number;
  high_risk: number;
}

@Component({
  selector: 'app-dashboard-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-cards.html',
  styleUrl: './dashboard-cards.css'
})
export class DashboardCards implements OnInit {
  stats: VendorStats = {
    total: 0,
    approved: 0,
    pending_review: 0,
    suspended: 0,
    rejected: 0,
    high_risk: 0
  };
  loading = true;
  errorMsg = '';
  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}
}

const PLACEHOLDER_DASHBOARD_CARDS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderDashboardCards(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_DASHBOARD_CARDS_ROWS;
  }
  return rows.filter((row) => !!row);
}
