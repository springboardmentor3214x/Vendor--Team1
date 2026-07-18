import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-vendor-reliability',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './vendor-reliability.html',
  styleUrls: ['./vendor-reliability.css']
})
export class VendorReliability {
  vendors = [
    { name: 'TechCorp Solutions', category: 'IT Equipment', financial: 'Stable', operational: 'Low', risk: 'Low' },
    { name: 'Apex Suppliers Ltd.', category: 'Raw Materials', financial: 'Critical', operational: 'High', risk: 'High' },
    { name: 'Global Parts Co.', category: 'Maintenance', financial: 'Stable', operational: 'Medium', risk: 'Medium' },
    { name: 'Office Depot', category: 'Office Supplies', financial: 'Excellent', operational: 'Low', risk: 'Low' }
  ];
}