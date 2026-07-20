import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-procurement-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  templateUrl: './procurement-dashboard.html',
  styleUrl: './procurement-dashboard.css'
})
export class ProcurementDashboard {

  summaryCards = [

    {
      title: 'Total Requests',
      value: 28,
      color: '#2563eb'
    },

    {
      title: 'Pending Requests',
      value: 7,
      color: '#f59e0b'
    },

    {
      title: 'Approved Requests',
      value: 15,
      color: '#16a34a'
    },

    {
      title: 'Purchase Orders',
      value: 11,
      color: '#9333ea'
    },

    {
      title: 'Delivered Orders',
      value: 8,
      color: '#0f766e'
    },

    {
      title: 'Completed',
      value: 6,
      color: '#15803d'
    },

    {
      title: 'Cancelled',
      value: 2,
      color: '#dc2626'
    }

  ];

  recentActivities = [

    {
      message: 'PR-1001 created by IT Department'
    },

    {
      message: 'PR-1002 approved by Procurement Manager'
    },

    {
      message: 'PO-5001 generated successfully'
    },

    {
      message: 'Invoice INV-101 uploaded by Vendor'
    },

    {
      message: 'Delivery completed for PO-4998'
    }

  ];

}