import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

interface DeliveryRecord {
  poNumber: string;
  vendorName: string;
  expectedDate: string;
  actualDate: string;
  delayDays: number;
  status: 'Early Delivery' | 'On-Time Delivery' | 'Delayed Delivery';
  remarks: string;
}

@Component({
  selector: 'app-delivery-performance',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './delivery-performance.html',
  styleUrls: ['./delivery-performance.css']
})
export class DeliveryPerformance implements OnInit {
  records: DeliveryRecord[] = [];

  ngOnInit() {
    this.records = [
      this.calculateDelivery('PO-2023-101', 'TechCorp Solutions', '2023-10-15', '2023-10-14', 'Arrived early'),
      this.calculateDelivery('PO-2023-102', 'Global Logistics Inc.', '2023-10-18', '2023-10-18', 'As expected'),
      this.calculateDelivery('PO-2023-103', 'Prime Raw Materials', '2023-10-20', '2023-10-23', 'Traffic issues'),
      this.calculateDelivery('PO-2023-104', 'Office Depot', '2023-10-25', '2023-10-24', 'Prompt delivery'),
      this.calculateDelivery('PO-2023-105', 'TechCorp Solutions', '2023-10-30', '2023-11-02', 'Customs delay')
    ];
  }

  calculateDelivery(poNumber: string, vendorName: string, expected: string, actual: string, remarks: string): DeliveryRecord {
    const expectedDate = new Date(expected);
    const actualDate = new Date(actual);
    const diffTime = actualDate.getTime() - expectedDate.getTime();
    const delayDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    let status: 'Early Delivery' | 'On-Time Delivery' | 'Delayed Delivery' = 'On-Time Delivery';
    if (delayDays < 0) {
      status = 'Early Delivery';
    } else if (delayDays > 0) {
      status = 'Delayed Delivery';
    }

    return {
      poNumber,
      vendorName,
      expectedDate: expected,
      actualDate: actual,
      delayDays: delayDays > 0 ? delayDays : 0,
      status,
      remarks
    };
  }

  getStatusColor(status: string): string {
    switch(status) {
      case 'Early Delivery': return '#3b82f6';
      case 'On-Time Delivery': return '#34c759';
      case 'Delayed Delivery': return '#ff3b30';
      default: return '#8e8e93';
    }
  }
}
