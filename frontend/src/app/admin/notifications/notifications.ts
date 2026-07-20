import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './notifications.html',
  styleUrls: ['./notifications.css']
})
export class Notifications {
  markAllRead() { this.notifications.forEach(n => n.unread = false); }
  notifications = [
    { title: 'New Vendor Registration', message: 'TechCorp Solutions has submitted a registration request pending approval.', time: '10 mins ago', type: 'info', icon: 'domain_add', unread: true },
    { title: 'System Maintenance', message: 'Scheduled maintenance will occur on Sunday at 2:00 AM UTC.', time: '2 hours ago', type: 'alert', icon: 'warning', unread: true },
    { title: 'Weekly Backup Complete', message: 'The automated system backup was completed successfully.', time: '1 day ago', type: 'success', icon: 'cloud_done', unread: false },
    { title: 'User Role Updated', message: 'Admin modified permissions for John Doe.', time: '2 days ago', type: 'info', icon: 'manage_accounts', unread: false }
  ];
}