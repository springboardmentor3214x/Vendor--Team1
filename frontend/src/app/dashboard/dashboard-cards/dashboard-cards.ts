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
}

const PLACEHOLDER_DASHBOARD_CARDS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderDashboardCards(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_DASHBOARD_CARDS_ROWS;
}
