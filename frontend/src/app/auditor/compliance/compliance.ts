import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';
import { ContractService } from '../../core/services/contract.service';

@Component({
  selector: 'app-compliance',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './compliance.html',
  styleUrls: ['./compliance.css']
})
export class Compliance implements OnInit {
  isLoading = true;
  vendors: any[] = [];

  constructor(private contractService: ContractService) {}

  ngOnInit(): void {
    this.loadCompliance();
  }

  loadCompliance(): void {
    this.isLoading = true;
    this.contractService.getComplianceDashboard().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.expiring_certifications) {
          this.vendors = res.expiring_certifications.map((c: any) => ({
            name: c.certification_name || `Vendor #${c.vendor_id}`,
            category: c.issuing_authority || 'Compliance',
            iso: true,
            gdpr: true,
            status: c.status || 'Compliant'
          }));
        } else {
          this.vendors = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.vendors = [];
      }
    });
  }

  download() { window.print(); }
}