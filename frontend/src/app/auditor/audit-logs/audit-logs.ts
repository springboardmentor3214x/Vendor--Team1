import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';
import { CommunicationService } from '../../core/services/communication.service';

@Component({
  selector: 'app-audit-logs',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button, InputComponent, Table],
  templateUrl: './audit-logs.html',
  styleUrls: ['./audit-logs.css']
})
export class AuditLogs implements OnInit {
  loading = true;
  errorMsg = '';
  allLogs: any[] = [];
  logs: any[] = [];
  searchText = '';
  selectedModule = 'All';
  modules = ['All', 'Vendor', 'Procurement', 'Contract', 'Invoice', 'Compliance', 'Communication', 'Delivery', 'User'];
  constructor(private communicationService: CommunicationService) {}
}

const PLACEHOLDER_AUDIT_LOGS_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderAuditLogs(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_AUDIT_LOGS_ROWS;
  }
  return rows.filter((row) => !!row);
}
