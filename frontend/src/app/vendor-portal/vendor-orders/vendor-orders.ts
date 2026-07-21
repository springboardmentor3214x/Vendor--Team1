import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-vendor-orders',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './vendor-orders.html',
  styleUrls: ['./vendor-orders.css']
})
export class VendorOrders {
  orders = [
    { poNumber: 'PO-2023-1001', date: '2023-10-15', amount: 15400, deadline: '2023-11-01', status: 'In Transit' },
    { poNumber: 'PO-2023-0984', date: '2023-09-28', amount: 4200, deadline: '2023-10-10', status: 'Delivered' },
    { poNumber: 'PO-2023-0942', date: '2023-09-15', amount: 28500, deadline: '2023-10-05', status: 'Delivered' },
    { poNumber: 'PO-2023-1022', date: '2023-10-22', amount: 8900, deadline: '2023-11-15', status: 'Processing' }
  ];
}