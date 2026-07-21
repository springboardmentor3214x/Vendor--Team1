import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

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

  ngOnInit() {
    this.records = [
      this.calculateDuration('PO-2023-101', 'TechCorp Solutions', '2023-10-10T09:00:00Z', '2023-10-10T09:45:00Z', 'Clarification on specs provided quickly.'),
      this.calculateDuration('PO-2023-102', 'Global Logistics Inc.', '2023-10-11T14:00:00Z', '2023-10-11T16:30:00Z', 'Delayed due to timezone differences.'),
      this.calculateDuration('PO-2023-103', 'Prime Raw Materials', '2023-10-12T10:00:00Z', '2023-10-13T11:00:00Z', 'Took over a day to respond to missing item query.'),
      this.calculateDuration('PO-2023-104', 'Office Depot', '2023-10-15T08:00:00Z', '2023-10-15T08:15:00Z', 'Instant support available.')
    ];
  }

  calculateDuration(poNumber: string, vendorName: string, sent: string, response: string, remarks: string): CommRecord {
    const sentDate = new Date(sent);
    const responseDate = new Date(response);
    const diffMs = responseDate.getTime() - sentDate.getTime();
    
    const diffHrs = diffMs / (1000 * 60 * 60);
    const duration = diffHrs < 1 ? `${Math.round(diffMs / (1000 * 60))} Mins` : `${diffHrs.toFixed(1)} Hrs`;
    
    let status: 'Fast' | 'Acceptable' | 'Slow' | 'Unresponsive' = 'Acceptable';
    if (diffHrs <= 2) {
      status = 'Fast';
    } else if (diffHrs <= 12) {
      status = 'Acceptable';
    } else if (diffHrs <= 48) {
      status = 'Slow';
    } else {
      status = 'Unresponsive';
    }

    return { poNumber, vendorName, sentTime: sent, responseTime: response, responseDuration: duration, status, remarks };
  }

  getStatusColor(status: string): string {
    switch(status) {
      case 'Fast': return '#34c759';
      case 'Acceptable': return '#ff9500';
      case 'Slow': return '#ff3b30';
      case 'Unresponsive': return '#8e8e93';
      default: return '#8e8e93';
    }
  }
}
