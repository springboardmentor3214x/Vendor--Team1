import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-procurement-recommendations',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './procurement-recommendations.html',
  styleUrls: ['./procurement-recommendations.css']
})
export class ProcurementRecommendations implements OnInit {
  categories = ['All', 'IT Vendors', 'Raw Material Suppliers', 'Logistics Partners', 'Service Providers'];
  selectedCategory = 'All';
  recommendations: any[] = [];
  isLoading = true;
}

const PLACEHOLDER_PROCUREMENT_RECOMMENDATIONS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderProcurementRecommendations(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PROCUREMENT_RECOMMENDATIONS_ROWS;
}
