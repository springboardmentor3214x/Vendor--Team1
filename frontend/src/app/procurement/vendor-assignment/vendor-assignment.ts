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

  loadVendors(): void {
    this.isLoading = true;
    this.procurementService.getApprovedVendors().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (Array.isArray(res)) {
          this.vendors = res.map(v => {
            const score = v.reliability_score ?? 0;
            return {
              id: v.id,
              name: v.company_name || v.vendor_name,
              category: v.category || 'Supplier',
              contactPerson: v.contact_person || v.vendor_name,
              reliabilityScore: score,
              riskLevel: this.getRiskLevel(score),
              previousPerformance: v.quality_score ? Math.round(v.quality_score) : 0,
              deliveryRating: v.delivery_score ? (v.delivery_score / 20).toFixed(1) : '0.0',
              status: v.status || 'Active'
            };
          });
        } else {
          this.vendors = [];
        }
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error fetching vendors', err);
      }
    });
  }

  assignVendor(vendor: any): void {
    if (!this.requestId) return;

    const isHighRisk = vendor.riskLevel === 'High Risk';
    const prompt = isHighRisk
      ? `WARNING — HIGH RISK VENDOR\n\n${vendor.name} has a reliability score of ` +
        `${vendor.reliabilityScore.toFixed(1)} and is classified as High Risk. ` +
        `Past orders show delays, quality issues or slow communication.\n\n` +
        `Assign this vendor anyway?`
      : `Assign ${vendor.name} to this procurement request?`;

    if (!confirm(prompt)) return;

    this.procurementService.assignVendor(this.requestId, vendor.id.toString(), isHighRisk).subscribe({
      next: (res) => {
        if (res?.warning) {
          alert(res.warning);
        }
        if (confirm(`Vendor ${vendor.name} assigned successfully! Do you want to generate a Purchase Order now?`)) {
          this.router.navigate(['/procurement/purchase-order/create'], {
            queryParams: { pr: this.requestId, vendor: vendor.id }
          });
        } else {
          this.router.navigate(['/procurement/requests']);
        }
      },
      error: (err) => alert('Vendor assignment failed: ' + (err.error?.detail || err.message))
    });
  }

  getRiskLevel(score: number): 'Low Risk' | 'Medium Risk' | 'High Risk' {
    if (score >= 80) return 'Low Risk';
    if (score >= 50) return 'Medium Risk';
    return 'High Risk';
  }

  getBadgeVariant(score: number): 'success' | 'warning' | 'danger' {
    const level = this.getRiskLevel(score);
    if (level === 'Low Risk') return 'success';
    if (level === 'Medium Risk') return 'warning';
    return 'danger';
  }

  get highRiskCount(): number {
    return this.vendors.filter(v => v.riskLevel === 'High Risk').length;
  }
}
