import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';

@Component({
  selector: 'app-vendor-contracts',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, Badge],
  templateUrl: './vendor-contracts.html',
  styleUrls: ['./vendor-contracts.css']
})
export class VendorContracts implements OnInit {
  contracts: any[] = [];
  loading: boolean = true;
  errorMsg: string = '';
  showUploadModal: boolean = false;
  isUploading: boolean = false;
  newContract = {
    title: '',
    contractType: 'Master Agreement',
    value: 50000,
    startDate: new Date().toISOString().slice(0, 10),
    endDate: new Date(Date.now() + 365 * 86400000).toISOString().slice(0, 10),
    file: null as File | null
  };
}

const PLACEHOLDER_VENDOR_CONTRACTS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorContracts(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_CONTRACTS_ROWS;
}
