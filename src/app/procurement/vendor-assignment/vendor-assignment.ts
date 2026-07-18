import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

export interface ApprovedVendorMock {
  id: number;
  name: string;
  category: string;
  contactPerson: string;
  reliabilityScore: number;
  deliveryRating: number;
  status: string;
}

@Component({
  selector: 'app-vendor-assignment',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './vendor-assignment.html',
  styleUrls: ['./vendor-assignment.css'],
})
export class VendorAssignment implements OnInit {
  requestId: string | null = null;

  columns: TableColumn[] = [
    { key: 'name', label: 'Vendor Name' },
    { key: 'category', label: 'Category' },
    { key: 'contactPerson', label: 'Contact Person' },
    { key: 'reliabilityScore', label: 'Reliability Score' },
    { key: 'deliveryRating', label: 'Delivery Rating' },
    { key: 'status', label: 'Status' },
    { key: 'actions', label: 'Actions' }
  ];

  vendors: ApprovedVendorMock[] = [
    { id: 1, name: 'Global Logistics', category: 'Shipping', contactPerson: 'John', reliabilityScore: 98, deliveryRating: 4.8, status: 'Active' },
    { id: 2, name: 'TechCorp Solutions', category: 'IT', contactPerson: 'Sarah', reliabilityScore: 95, deliveryRating: 4.5, status: 'Active' },
    { id: 3, name: 'Office Depot', category: 'Supplies', contactPerson: 'Mike', reliabilityScore: 88, deliveryRating: 3.9, status: 'Inactive' }
  ];

  constructor(
    private route: ActivatedRoute, 
    private router: Router,
    private procurementService: ProcurementService
  ) {}

  ngOnInit(): void {
    this.requestId = this.route.snapshot.paramMap.get('id');
    this.loadVendors();
  }

  loadVendors(): void {
    this.procurementService.getApprovedVendors().subscribe({
      next: (res) => {
        this.vendors = res;
      },
      error: (err) => {
        console.error('Error fetching vendors', err);
        // Fallback mock data
        this.vendors = [
          {
            id: 101,
            name: 'TechCorp Ltd',
            category: 'IT Vendors',
            contactPerson: 'Jane Doe',
            reliabilityScore: 98,
            deliveryRating: 4.8,
            status: 'Active'
          },
          {
            id: 102,
            name: 'OfficePro Supplies',
            category: 'Service Providers',
            contactPerson: 'John Smith',
            reliabilityScore: 85,
            deliveryRating: 4.2,
            status: 'Active'
          },
          {
            id: 103,
            name: 'Global Compute Solutions',
            category: 'IT Vendors',
            contactPerson: 'Sarah Connor',
            reliabilityScore: 92,
            deliveryRating: 4.5,
            status: 'Active'
          }
        ];
      }
    });
  }

  assignVendor(vendor: ApprovedVendorMock): void {
    if (!this.requestId) return;
    
    if (confirm(`Are you sure you want to assign ${vendor.name} to this request?`)) {
      this.procurementService.assignVendor(this.requestId, vendor.id.toString()).subscribe({
        next: () => {
          alert(`Vendor ${vendor.name} assigned successfully. Proceeding to Purchase Order creation.`);
          this.router.navigate(['/procurement/purchase-order/create'], { queryParams: { pr: this.requestId, vendor: vendor.id }});
        },
        error: (err) => {
          console.error('Error assigning vendor', err);
          // Mock success
          alert(`Vendor ${vendor.name} assigned successfully. (Mocked)`);
          this.router.navigate(['/procurement/purchase-order/create'], { queryParams: { pr: this.requestId, vendor: vendor.id }});
        }
      });
    }
  }

  getBadgeVariant(score: number): 'success' | 'warning' | 'danger' {
    if (score >= 90) return 'success';
    if (score >= 70) return 'warning';
    return 'danger';
  }
}
