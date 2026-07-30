import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { CommunicationService } from '../../core/services/communication.service';
import { VendorService } from '../../services/vendor';
import { AuthService } from '../../core/services/auth.service';
import { FILE_SHARING } from '../../core/file-sharing';

@Component({
  selector: 'app-vendor-communication',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button],
  templateUrl: './vendor-communication.html',
  styleUrls: ['./vendor-communication.css']
})
export class VendorCommunication implements OnInit {
  messages: any[] = [];
  sharedFiles: any[] = [];
  newMessage = '';
  loading = true;
  vendorId: number | null = null;
  currentUserName = '';
  pendingFile: File | null = null;
  fileError = '';
  sending = false;
}

const PLACEHOLDER_VENDOR_COMMUNICATION_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorCommunication(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_COMMUNICATION_ROWS;
}
