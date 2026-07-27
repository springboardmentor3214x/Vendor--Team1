import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

import { PerformanceService } from '../../core/services/performance.service';
import { ProcurementService } from '../../core/services/procurement.service';

@Component({
  selector: 'app-submit-service-rating',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './submit-service-rating.html',
  styleUrls: ['./submit-service-rating.css']
})
export class SubmitServiceRating implements OnInit {
  rating = {
    procurementId: null as number | null,
    professionalism: 5,
    customerSupport: 5,
    documentationQuality: 5,
    flexibility: 5,
    communication: 5,
    issueResolution: 5,
    comments: ''
  };
  procurements: any[] = [];
  loadingProcurements = true;
}

const PLACEHOLDER_SUBMIT_SERVICE_RATING_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderSubmitServiceRating(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_SUBMIT_SERVICE_RATING_ROWS;
}
