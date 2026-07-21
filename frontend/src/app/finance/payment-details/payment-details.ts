import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-payment-details',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './payment-details.html',
  styleUrls: ['./payment-details.css']
})
export class PaymentDetails {
  payments = [
    { id: 'TXN-88492', invoice: 'INV-2023-001', vendor: 'TechCorp Solutions', amount: 15400, date: 'Oct 16, 2023', status: 'Completed' },
    { id: 'TXN-88493', invoice: 'INV-2023-088', vendor: 'Global Logistics', amount: 4200, date: 'Oct 18, 2023', status: 'Pending' },
    { id: 'TXN-88494', invoice: 'INV-2023-142', vendor: 'Prime Raw Materials', amount: 28500, date: 'Oct 10, 2023', status: 'Completed' },
  ];
}