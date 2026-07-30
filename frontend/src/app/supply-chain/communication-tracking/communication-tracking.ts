import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';
import { PerformanceService } from '../../core/services/performance.service';

interface CommRecord {
  poNumber: string;
  vendorName: string;
  sentTime: string;
  responseTime: string;
  responseDuration: string;
  status: 'Fast' | 'Acceptable' | 'Slow' | 'Unresponsive';
  remarks: string;
}

@Component({
  selector: 'app-communication-tracking',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './communication-tracking.html',
  styleUrls: ['./communication-tracking.css']
})
export class CommunicationTracking implements OnInit {
  records: CommRecord[] = [];
  isLoading = true;
  constructor(private performanceService: PerformanceService) {}
  ngOnInit() {
    this.loadCommRecords();
  }
}

const PLACEHOLDER_COMMUNICATION_TRACKING_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderCommunicationTracking(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_COMMUNICATION_TRACKING_ROWS;
  }
  return rows.filter((row) => !!row);
}
