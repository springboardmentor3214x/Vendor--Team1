import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-vendor-performance-details',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './vendor-performance-details.html',
  styleUrls: ['./vendor-performance-details.css']
})
export class VendorPerformanceDetails implements OnInit {
  vendorId: string = '';
  
  vendor: any = {
    id: 'VND-001',
    name: 'TechCorp Solutions',
    category: 'IT Equipment',
    rating: 5,
    score: 4.9
  };

  deliveryHistory = [
    { month: 'May', onTime: 92 },
    { month: 'Jun', onTime: 94 },
    { month: 'Jul', onTime: 98 },
    { month: 'Aug', onTime: 95 },
    { month: 'Sep', onTime: 99 },
    { month: 'Oct', onTime: 100 }
  ];

  recentOrders = [
    { po: 'PO-2023-1001', date: 'Oct 15, 2023', delivery: 'On-Time', quality: true, rating: 5 },
    { po: 'PO-2023-0984', date: 'Sep 28, 2023', delivery: 'On-Time', quality: true, rating: 4 },
    { po: 'PO-2023-0912', date: 'Aug 10, 2023', delivery: 'Delayed', quality: true, rating: 3 },
    { po: 'PO-2023-0850', date: 'Jul 22, 2023', delivery: 'On-Time', quality: true, rating: 5 }
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id') || 'VND-001';
  }
}
