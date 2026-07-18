import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-vendor-performance',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button, Table],
  templateUrl: './vendor-performance.html',
  styleUrls: ['./vendor-performance.css']
})
export class VendorPerformance {
  topVendors = [
    { id: 'VND-001', name: 'TechCorp Solutions', category: 'IT Equipment', rating: 5, onTime: '99%', score: '4.9' },
    { id: 'VND-002', name: 'Global Logistics Inc.', category: 'Services', rating: 4, onTime: '94%', score: '4.5' },
    { id: 'VND-003', name: 'Prime Raw Materials', category: 'Raw Materials', rating: 4, onTime: '95%', score: '4.2' },
    { id: 'VND-004', name: 'Office Depot', category: 'Office Supplies', rating: 3, onTime: '88%', score: '3.9' }
  ];
}