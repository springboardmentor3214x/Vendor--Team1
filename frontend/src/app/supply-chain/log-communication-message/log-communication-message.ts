import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { CommunicationService } from '../../core/services/communication.service';

@Component({
  selector: 'app-log-communication-message',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './log-communication-message.html',
  styleUrls: ['./log-communication-message.css']
})
export class LogCommunicationMessage implements OnInit {
  message = {
    poNumber: '',
    vendorName: '',
    subject: '',
    sentTime: '',
    responseTime: '',
    remarks: ''
  };
  formError: string = '';
}

const PLACEHOLDER_LOG_COMMUNICATION_MESSAGE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderLogCommunicationMessage(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_LOG_COMMUNICATION_MESSAGE_ROWS;
}
