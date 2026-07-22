import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-vendor-assignment',
  standalone: true,
  imports: [CommonModule, RouterModule, Table, Badge, Button],
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

  vendors: any[] = [];

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
        this.vendors = res.map(v => ({
          id: v.id,
          name: v.company_name,
          category: v.category,
          contactPerson: v.vendor_name,
          reliabilityScore: v.reliability_score || 0,
          deliveryRating: v.delivery_score || 0,
          status: v.status
        }));
      }
    });
  }

  assignVendor(vendor: any): void {
    if (!this.requestId) return;
    if (confirm(`Assign ${vendor.name} to this request?`)) {
      this.procurementService.assignVendor(this.requestId, vendor.id.toString()).subscribe({
        next: () => {
          alert(`Vendor ${vendor.name} assigned.`);
          this.router.navigate(['/procurement/requests']);
        },
        error: () => alert('Vendor assignment failed.')
      });
    }
  }

  getBadgeVariant(score: number): 'success' | 'warning' | 'danger' {
    if (score >= 90) return 'success';
    if (score >= 70) return 'warning';
    return 'danger';
  }
}
