import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-audit-logs',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './audit-logs.html',
  styleUrls: ['./audit-logs.css']
})
export class AuditLogs {
  logs = [
    { timestamp: '2023-10-25 14:32:01', user: 'Alice Smith', role: 'Administrator', action: 'UPDATE_ROLE', entity: 'User: USR-003', ip: '192.168.1.45' },
    { timestamp: '2023-10-25 14:15:22', user: 'Bob Johnson', role: 'Procurement Mgr', action: 'APPROVE_PO', entity: 'PO: PO-2023-1001', ip: '10.0.0.12' },
    { timestamp: '2023-10-25 13:45:09', user: 'Diana Evans', role: 'Vendor', action: 'UPLOAD_DOC', entity: 'Contract: NDA.pdf', ip: '172.16.254.1' },
    { timestamp: '2023-10-25 11:20:00', user: 'SYSTEM', role: 'System', action: 'AUTO_BACKUP', entity: 'Database', ip: '127.0.0.1' },
  ];
}