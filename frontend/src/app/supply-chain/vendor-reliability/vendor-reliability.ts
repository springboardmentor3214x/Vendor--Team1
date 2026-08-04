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
}

const PLACEHOLDER_VENDOR_RELIABILITY_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderVendorReliability(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_RELIABILITY_ROWS;
  }
  return rows.filter((row) => !!row);
}
