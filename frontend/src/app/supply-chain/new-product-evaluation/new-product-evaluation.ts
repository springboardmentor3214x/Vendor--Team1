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
  selector: 'app-new-product-evaluation',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './new-product-evaluation.html',
  styleUrls: ['./new-product-evaluation.css']
})
export class NewProductEvaluation implements OnInit {
  evaluation = {
    procurementId: null as number | null,
    inspectionDate: new Date().toISOString().slice(0, 10),
    materialQuality: 5,
    packagingQuality: 5,
    quantityAccuracy: 5,
    specCompliance: 5,
    defectCount: 0,
    remarks: ''
  };
  procurements: any[] = [];
  loadingProcurements = true;
  formError = '';
}

const PLACEHOLDER_NEW_PRODUCT_EVALUATION_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderNewProductEvaluation(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_NEW_PRODUCT_EVALUATION_ROWS;
}
