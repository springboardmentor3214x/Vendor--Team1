import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { CommunicationService } from '../../core/services/communication.service';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-supply-chain-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './supply-chain-dashboard.html',
  styleUrls: ['./supply-chain-dashboard.css'],
})
export class SupplyChainDashboard implements OnInit {
  columns: TableColumn[] = [
    { key: 'date', label: 'Date' },
    { key: 'activity', label: 'Activity' },
    { key: 'status', label: 'Status' }
  ];
  recentActivities: any[] = [];
  isLoading = true;
  avgReliabilityScore = 0;
  onTimeDelivery = 0;
  defectRate = 0;
  atRiskVendors = 0;
  constructor(
    private commService: CommunicationService,
    private reliabilityService: ReliabilityService
  ) {}
}

const PLACEHOLDER_SUPPLY_CHAIN_DASHBOARD_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderSupplyChainDashboard(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_SUPPLY_CHAIN_DASHBOARD_ROWS;
  }
  return rows.filter((row) => !!row);
}
