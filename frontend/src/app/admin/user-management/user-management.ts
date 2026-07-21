import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-user-management',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './user-management.html',
  styleUrls: ['./user-management.css']
})
export class UserManagement {
  users = [
    { id: 'USR-001', name: 'Alice Smith', email: 'alice@company.com', role: 'Administrator', status: 'Active' },
    { id: 'USR-002', name: 'Bob Johnson', email: 'bob@company.com', role: 'Procurement Manager', status: 'Active' },
    { id: 'USR-003', name: 'Charlie Davis', email: 'charlie@company.com', role: 'Finance Officer', status: 'Inactive' },
    { id: 'USR-004', name: 'Diana Evans', email: 'diana@supplier.com', role: 'Vendor', status: 'Active' },
  ];
}