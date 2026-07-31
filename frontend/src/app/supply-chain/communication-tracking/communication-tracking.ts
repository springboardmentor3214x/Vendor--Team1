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

  loadCommRecords() {
    this.isLoading = true;
    this.performanceService.getCommunicationRecords(1).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.length > 0) {
          this.records = res.map((c: any) => {
            const hrs = c.response_duration_hours || 0;
            let status: 'Fast' | 'Acceptable' | 'Slow' | 'Unresponsive' = 'Fast';
            if (hrs > 24) status = 'Unresponsive';
            else if (hrs > 12) status = 'Slow';
            else if (hrs > 4) status = 'Acceptable';

            return {
              poNumber: `PO-${1000 + (c.procurement_id || c.id)}`,
              vendorName: `Vendor #${c.vendor_id}`,
              sentTime: c.message_sent_time ? new Date(c.message_sent_time).toLocaleString() : 'N/A',
              responseTime: c.vendor_response_time ? new Date(c.vendor_response_time).toLocaleString() : 'N/A',
              responseDuration: `${hrs.toFixed(1)} Hrs`,
              status,
              remarks: c.remarks || 'Logged'
            };
          });
        } else {
          this.records = [];
        }
      },
      error: () => {
        this.isLoading = false;
        this.records = [];
      }
    });
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
