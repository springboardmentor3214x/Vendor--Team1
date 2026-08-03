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
  uploading = false;
  showFilesPanel = false;
  readonly allowedExtensions = FILE_SHARING.allowedExtensions;
  readonly maxFileSizeBytes = FILE_SHARING.maxSizeBytes;
  readonly acceptAttr = FILE_SHARING.acceptAttr;
  constructor(
    private commService: CommunicationService,
    private vendorService: VendorService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}
  ngOnInit(): void {
    const user = this.authService.getCurrentUser();
    this.currentUserName = user?.fullName || user?.email || 'Vendor';

    this.vendorService.getMyVendorProfile().subscribe({
      next: (v) => {
        if (v) this.vendorId = v.id;
        this.loadMessages();
        this.loadFiles();
      },
      error: () => this.loadMessages()
    });
  }
  loadMessages(): void {
    this.loading = true;
    this.commService.getMessages(this.vendorId || undefined).subscribe({
      next: (data) => {
        this.loading = false;
        this.messages = (data || []).map(m => ({
          id: m.id,
          sender: m.sender_name || 'System User',
          content: m.message || '',
          fileName: m.file_name || null,
          isRead: m.is_read,
          timestamp: m.sent_at
            ? new Date(m.sent_at).toLocaleString([], { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })
            : 'Just now',

          isSelf: (m.sender_name || '') === this.currentUserName
        }));

        this.commService.markMessagesRead({ vendor_id: this.vendorId || undefined }).subscribe({
          error: () => undefined
        });

        this.cdr.markForCheck();
      },
      error: () => {
        this.loading = false;
        this.cdr.markForCheck();
      }
    });
  }
}

const PLACEHOLDER_VENDOR_COMMUNICATION_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 6, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 7, name: 'Northwind Steel', status: 'Active' },
  { id: 8, name: 'Orbit IT Systems', status: 'Pending Approval' },
];

function usePlaceholderVendorCommunication(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_VENDOR_COMMUNICATION_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
