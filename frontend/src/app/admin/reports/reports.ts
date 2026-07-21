import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './reports.html',
  styleUrls: ['./reports.css']
})
export class Reports {
  exportCSV() { alert("Report downloaded successfully!"); }
  reports = [
    { title: 'User Activity Log', desc: 'Detailed log of all user logins, actions, and system access.', icon: 'manage_accounts' },
    { title: 'Role Distribution', desc: 'Breakdown of active users across all system roles.', icon: 'pie_chart' },
    { title: 'Vendor Onboarding', desc: 'Monthly statistics of new vendor registrations and approvals.', icon: 'how_to_reg' },
    { title: 'System Errors', desc: 'Compilation of system errors, warnings, and failed API requests.', icon: 'bug_report' }
  ];
}