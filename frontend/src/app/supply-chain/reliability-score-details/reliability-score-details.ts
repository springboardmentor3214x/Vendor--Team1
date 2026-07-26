import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-reliability-score-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button],
  templateUrl: './reliability-score-details.html',
  styleUrls: ['./reliability-score-details.css']
})
export class ReliabilityScoreDetails implements OnInit {
  vendorId: string | null = '';
  vendorName: string = 'Loading...';
  overallScore: number = 0;
}

const PLACEHOLDER_RELIABILITY_SCORE_DETAILS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderReliabilityScoreDetails(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_RELIABILITY_SCORE_DETAILS_ROWS;
}
