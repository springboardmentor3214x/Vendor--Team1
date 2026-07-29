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
}

const PLACEHOLDER_VENDOR_RELIABILITY_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderVendorReliability(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_RELIABILITY_ROWS;
}
