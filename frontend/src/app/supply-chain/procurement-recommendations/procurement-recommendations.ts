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
  constructor(private reliabilityService: ReliabilityService) {}
  ngOnInit(): void {
    this.loadRecommendations();
  }
}

const PLACEHOLDER_PROCUREMENT_RECOMMENDATIONS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderProcurementRecommendations(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PROCUREMENT_RECOMMENDATIONS_ROWS;
  }
  return rows.filter((row) => !!row);
}
