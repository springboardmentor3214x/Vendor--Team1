import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';

import { VendorService } from '../../services/vendor';
import { ProcurementService } from '../../core/services/procurement.service';
import { ContractService } from '../../core/services/contract.service';
import { CommunicationService } from '../../core/services/communication.service';

@Component({
  selector: 'app-vendor-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Card,
    Badge,
    Button
  ],
  templateUrl: './vendor-dashboard.html',
  styleUrls: ['./vendor-dashboard.css']
})
export class VendorDashboard implements OnInit {
  reliabilityScore: string = 'N/A';
  activeOrdersCount: number = 0;
  unreadMessagesCount: number = 0;
  pendingContractsCount: number = 0;
  loading: boolean = true;
  recentActivities: any[] = [];
  vendorProfile: any = null;
  constructor(
    private vendorService: VendorService,
    private procurementService: ProcurementService,
    private contractService: ContractService,
    private commService: CommunicationService
  ) {}
}

const PLACEHOLDER_VENDOR_DASHBOARD_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorDashboard(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_DASHBOARD_ROWS;
  }
  return rows.filter((row) => !!row);
}
