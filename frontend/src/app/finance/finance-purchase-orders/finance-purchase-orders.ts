import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-finance-purchase-orders',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './finance-purchase-orders.html',
  styleUrls: ['./finance-purchase-orders.css']
})
export class FinancePurchaseOrders {
  filter() { alert("Filter applied"); }
  export() { alert("Exported CSV"); }
  viewPO() { alert("Viewing PO Details"); }

  orders = [
    { poNumber: 'PO-2023-1001', dept: 'IT Infrastructure', vendor: 'TechCorp', budgetCode: 'BGT-IT-23', amount: 15400, status: 'Approved' },
    { poNumber: 'PO-2023-1002', dept: 'Marketing', vendor: 'DesignStudio', budgetCode: 'BGT-MKT-23', amount: 8500, status: 'Pending Review' },
    { poNumber: 'PO-2023-1003', dept: 'Operations', vendor: 'Global Logistics', budgetCode: 'BGT-OPS-23', amount: 4200, status: 'Approved' },
  ];
}