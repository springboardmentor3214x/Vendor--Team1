import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-auditor-reports',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './auditor-reports.html',
  styleUrls: ['./auditor-reports.css']
})
export class AuditorReports {
  reports = [
    { title: 'Q3 Financial Procurement Audit', type: 'Financial', date: 'Oct 01, 2023', status: 'Completed' },
    { title: 'ISO Vendor Compliance Check', type: 'Compliance', date: 'Oct 15, 2023', status: 'In Progress' },
    { title: 'System Access Security Review', type: 'Security', date: 'Nov 01, 2023', status: 'Scheduled' },
  ];
}