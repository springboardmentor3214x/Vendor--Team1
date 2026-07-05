import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Badge } from '../../ui/badge/badge';
import { ContractService } from '../../core/services/contract.service';

@Component({
  selector: 'app-contract-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Badge],
  templateUrl: './contract-details.html',
  styleUrls: ['./contract-details.css']
})
export class ContractDetails implements OnInit {
  contract: any = null;
  certifications: any[] = [];
  compliance: any[] = [];
  loading = true;
}

const PLACEHOLDER_CONTRACT_DETAILS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderContractDetails(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_CONTRACT_DETAILS_ROWS;
}
