import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { Table, TableColumn } from '../../ui/table/table';
import { Badge } from '../../ui/badge/badge';
import { Button } from '../../ui/button/button';
import { ProcurementService } from '../../core/services/procurement.service';

export interface ProcurementRequestMock {
  id: number;
  requestNumber: string;
  title: string;
  department: string;
  requestedBy: string;
  vendor: string;
  priority: string;
  budget: number;
  status: string;
  createdDate: string;
}

@Component({
  selector: 'app-procurement-request-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    Table,
    Badge,
    Button
  ],
  templateUrl: './procurement-request-list.html',
  styleUrls: ['./procurement-request-list.css'],
})
export class ProcurementRequestList implements OnInit {
  columns: TableColumn[] = [
    { key: 'requestNumber', label: 'Request Number' },
    { key: 'title', label: 'Title' },
    { key: 'department', label: 'Department' },
    { key: 'requestedBy', label: 'Requested By' },
    { key: 'vendor', label: 'Vendor' },
    { key: 'priority', label: 'Priority' },
    { key: 'budget', label: 'Budget' },
    { key: 'status', label: 'Status' },
    { key: 'createdDate', label: 'Created Date' },
    { key: 'actions', label: 'Actions' }
  ];

  requests: ProcurementRequestMock[] = [
    { id: 1, requestNumber: 'PR-9001', title: 'New Laptops for Engineering Team', department: 'IT', requestedBy: 'Alice', vendor: 'TechCorp', priority: 'High', budget: 15000, status: 'Approved', createdDate: '2026-07-05' },
    { id: 2, requestNumber: 'PR-9002', title: 'Office Chairs and Desks', department: 'HR', requestedBy: 'Bob', vendor: 'Office Depot', priority: 'Medium', budget: 3500, status: 'Pending', createdDate: '2026-07-12' },
    { id: 3, requestNumber: 'PR-9003', title: 'Server Maintenance Contract', department: 'IT', requestedBy: 'Alice', vendor: 'IT Serve', priority: 'Critical', budget: 50000, status: 'Rejected', createdDate: '2026-07-16' }
  ];
  
  constructor(private procurementService: ProcurementService) {}

  ngOnInit(): void {
    this.loadRequests();
  }

  loadRequests(): void {
    this.procurementService.getAllProcurementRequests().subscribe({
      next: (res) => {
        this.requests = res;
      },
      error: (err) => {
        console.error('Error fetching procurement requests', err);
        // Fallback mock data with comprehensive examples
        this.requests = [
          {
            id: 1,
            requestNumber: 'PR-1024',
            title: 'Office Supplies Q3',
            department: 'Administration',
            requestedBy: 'Alice Smith',
            vendor: 'OfficePro Supplies',
            priority: 'Low',
            budget: 50000,
            status: 'Pending',
            createdDate: '15 Jul 2026'
          },
          {
            id: 2,
            requestNumber: 'PR-1025',
            title: 'Laptops for Engineering',
            department: 'Engineering',
            requestedBy: 'Bob Johnson',
            vendor: 'Compute Solutions',
            priority: 'High',
            budget: 2500000,
            status: 'Approved',
            createdDate: '14 Jul 2026'
          },
          {
            id: 3,
            requestNumber: 'PR-1026',
            title: 'Cloud Server Infrastructure',
            department: 'IT Operations',
            requestedBy: 'Sarah Connor',
            vendor: 'Global Compute Solutions',
            priority: 'Critical',
            budget: 8500000,
            status: 'Pending',
            createdDate: '16 Jul 2026'
          },
          {
            id: 4,
            requestNumber: 'PR-1027',
            title: 'Marketing Event Materials',
            department: 'Marketing',
            requestedBy: 'James Wilson',
            vendor: 'PrintWorks Ltd',
            priority: 'Medium',
            budget: 125000,
            status: 'Rejected',
            createdDate: '12 Jul 2026'
          },
          {
            id: 5,
            requestNumber: 'PR-1028',
            title: 'Office Chairs Replacement',
            department: 'Facilities',
            requestedBy: 'Emma Davis',
            vendor: 'Furniture Co',
            priority: 'Low',
            budget: 350000,
            status: 'Approved',
            createdDate: '10 Jul 2026'
          }
        ];
      }
    });
  }

  getBadgeVariant(status: string): 'success' | 'warning' | 'primary' | 'danger' | 'default' {
    if (status === 'Approved') return 'success';
    if (status === 'Pending') return 'warning';
    if (status === 'Rejected' || status === 'Critical') return 'danger';
    if (status === 'High' || status === 'Medium') return 'primary';
    return 'default';
  }

  deleteRequest(id: number): void {
    if (confirm('Are you sure you want to delete this procurement request?')) {
      this.procurementService.deleteProcurementRequest(id.toString()).subscribe({
        next: () => {
          this.requests = this.requests.filter(r => r.id !== id);
        },
        error: (err) => {
          console.error('Error deleting request', err);
          // Mock delete
          this.requests = this.requests.filter(r => r.id !== id);
        }
      });
    }
  }

  editRequest(r: any): void {
    alert("Editing request: " + r.requestNumber);
  }
}
