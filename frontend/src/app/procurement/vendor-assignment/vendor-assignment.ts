import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { Card } from '../../ui/card/card';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-vendor-assignment',
  standalone: true,
  imports: [CommonModule, RouterModule, Badge, Button, Card],
  templateUrl: './vendor-assignment.html',
  styleUrls: ['./vendor-assignment.css'],
})
export class VendorAssignment implements OnInit {
  requestId: string | null = null;
  requestDetails: any = null;
  vendors: any[] = [];
  isLoading = true;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private procurementService: ProcurementService
  ) {}
}

const PLACEHOLDER_VENDOR_ASSIGNMENT_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorAssignment(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_ASSIGNMENT_ROWS;
}
