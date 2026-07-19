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
  ngOnInit(): void {
    this.requestId = this.route.snapshot.paramMap.get('id');
    if (this.requestId) {
      this.loadRequestDetails(this.requestId);
    }
    this.loadVendors();
  }
  loadRequestDetails(id: string): void {
    this.procurementService.getProcurementRequestById(id).subscribe({
      next: (res) => this.requestDetails = res,
      error: (err) => console.error('Error loading request', err)
    });
  }
}

const PLACEHOLDER_VENDOR_ASSIGNMENT_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendorAssignment(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_ASSIGNMENT_ROWS;
  }
  return rows.filter((row) => !!row);
}
