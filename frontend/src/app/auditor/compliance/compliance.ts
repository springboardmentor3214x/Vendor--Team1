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
}

const PLACEHOLDER_COMPLIANCE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderCompliance(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_COMPLIANCE_ROWS;
}
