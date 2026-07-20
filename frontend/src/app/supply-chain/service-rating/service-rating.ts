import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

interface ServiceRecord {
  poNumber: string;
  vendorName: string;
  professionalism: number;
  customerSupport: number;
  documentationQuality: number;
  flexibility: number;
  communicationEffectiveness: number;
  issueResolution: number;
  overallRating: number;
  comments: string;
}

@Component({
  selector: 'app-service-rating',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './service-rating.html',
  styleUrls: ['./service-rating.css']
})
export class ServiceRating implements OnInit {
  ratings: ServiceRecord[] = [];

  ngOnInit() {
    this.ratings = [
      {
        poNumber: 'PO-2023-101',
        vendorName: 'TechCorp Solutions',
        professionalism: 5,
        customerSupport: 5,
        documentationQuality: 4,
        flexibility: 5,
        communicationEffectiveness: 5,
        issueResolution: 5,
        overallRating: 4.8,
        comments: 'Outstanding service throughout the cycle.'
      },
      {
        poNumber: 'PO-2023-103',
        vendorName: 'Prime Raw Materials',
        professionalism: 4,
        customerSupport: 3,
        documentationQuality: 3,
        flexibility: 4,
        communicationEffectiveness: 3,
        issueResolution: 4,
        overallRating: 3.5,
        comments: 'Good effort, but communication needs improvement.'
      }
    ];
  }
}
