import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

interface QualityEvaluation {
  poNumber: string;
  vendorName: string;
  inspectionDate: string;
  materialQuality: number;
  packagingQuality: number;
  quantityAccuracy: number;
  specCompliance: number;
  productDefects: string;
  overallRating: number;
  remarks: string;
}

@Component({
  selector: 'app-product-quality',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './product-quality.html',
  styleUrls: ['./product-quality.css']
})
export class ProductQuality implements OnInit {
  evaluations: QualityEvaluation[] = [];

  ngOnInit() {
    this.evaluations = [
      {
        poNumber: 'PO-2023-101',
        vendorName: 'TechCorp Solutions',
        inspectionDate: '2023-10-15',
        materialQuality: 5,
        packagingQuality: 5,
        quantityAccuracy: 5,
        specCompliance: 5,
        productDefects: 'None',
        overallRating: 5,
        remarks: 'Excellent quality all around'
      },
      {
        poNumber: 'PO-2023-103',
        vendorName: 'Prime Raw Materials',
        inspectionDate: '2023-10-24',
        materialQuality: 4,
        packagingQuality: 3,
        quantityAccuracy: 5,
        specCompliance: 4,
        productDefects: 'Minor dents on outer packaging',
        overallRating: 4,
        remarks: 'Good overall, but packaging can be improved'
      },
      {
        poNumber: 'PO-2023-104',
        vendorName: 'Office Depot',
        inspectionDate: '2023-10-25',
        materialQuality: 3,
        packagingQuality: 4,
        quantityAccuracy: 4,
        specCompliance: 3,
        productDefects: 'Some items not as sturdy as expected',
        overallRating: 3,
        remarks: 'Average quality'
      }
    ];
  }
}
