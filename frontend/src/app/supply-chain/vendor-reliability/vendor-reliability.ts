import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-vendor-reliability',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './vendor-reliability.html',
  styleUrls: ['./vendor-reliability.css']
})
export class VendorReliability implements OnInit {
  isLoading = true;
  vendors: any[] = [];

  constructor(private reliabilityService: ReliabilityService) {}

  ngOnInit(): void {
    this.loadRiskAssessment();
  }

  loadRiskAssessment(): void {
    this.isLoading = true;
    this.reliabilityService.getRiskAssessment().subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res) {
          const list: any[] = [];
          (res.low_risk_vendors || []).forEach((v: any) => {
            list.push({ name: v.company_name || v.vendor_name, category: v.category || 'General', financial: 'Stable', operational: 'Low Risk', risk: 'Low' });
          });
          (res.medium_risk_vendors || []).forEach((v: any) => {
            list.push({ name: v.company_name || v.vendor_name, category: v.category || 'General', financial: 'Fair', operational: 'Medium Risk', risk: 'Medium' });
          });
          (res.high_risk_vendors || []).forEach((v: any) => {
            list.push({ name: v.company_name || v.vendor_name, category: v.category || 'General', financial: 'Attention Needed', operational: 'High Risk', risk: 'High' });
          });
          this.vendors = list;
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });
  }
}