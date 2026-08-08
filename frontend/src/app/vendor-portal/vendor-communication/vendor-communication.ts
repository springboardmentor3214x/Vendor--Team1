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

  loadFiles(): void {
    this.commService.getFiles({ vendorId: this.vendorId || undefined }).subscribe({
      next: (files) => {
        this.sharedFiles = (files || []).map(f => ({
          ...f,
          sizeLabel: FILE_SHARING.formatSize(f.file_size),
          icon: FILE_SHARING.iconFor(f.file_name),
          uploadedOn: f.created_at ? new Date(f.created_at).toLocaleDateString() : '-'
        }));
        this.cdr.markForCheck();
      },
      error: () => {
        this.sharedFiles = [];
        this.cdr.markForCheck();
      }
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.fileError = '';
    this.pendingFile = null;

    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    const problem = FILE_SHARING.validate(file);
    if (problem) {
      this.fileError = problem;
      input.value = '';
      return;
    }
    this.pendingFile = file;
  }

  clearAttachment(): void {
    this.pendingFile = null;
    this.fileError = '';
  }

  sendMessage(): void {
    const content = this.newMessage.trim();
    if (!content && !this.pendingFile) return;

    this.sending = true;
    this.fileError = '';

    const done = () => {
      this.sending = false;
      this.newMessage = '';
      this.pendingFile = null;
      this.loadMessages();
      this.loadFiles();
    };
    const fail = (err: any) => {
      this.sending = false;
      this.fileError = err.error?.detail || 'Could not send the message.';
      this.cdr.markForCheck();
    };

    if (this.pendingFile) {

      const form = new FormData();
      form.append('message', content || `Shared a file: ${this.pendingFile.name}`);
      if (this.vendorId) form.append('vendor_id', String(this.vendorId));
      form.append('file', this.pendingFile);
      this.commService.sendMessageWithFile(form).subscribe({ next: done, error: fail });
    } else {
      const payload: any = { message: content };
      if (this.vendorId) payload.vendor_id = this.vendorId;
      this.commService.sendMessage(payload).subscribe({ next: done, error: fail });
    }
  }

  downloadAttachment(msg: any): void {
    this.commService.downloadMessageAttachment(msg.id).subscribe({
      next: (blob) => FILE_SHARING.saveBlob(blob, msg.fileName),
      error: () => this.fileError = 'Could not download the attachment.'
    });
  }

  downloadSharedFile(file: any): void {
    this.commService.downloadSharedFile(file.id).subscribe({
      next: (blob) => FILE_SHARING.saveBlob(blob, file.file_name),
      error: () => this.fileError = 'Could not download the file.'
    });
  }

  uploadStandaloneFile(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.fileError = '';
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    const problem = FILE_SHARING.validate(file);
    if (problem) {
      this.fileError = problem;
      input.value = '';
      return;
    }

    this.uploading = true;
    const form = new FormData();
    form.append('file', file);
    if (this.vendorId) form.append('vendor_id', String(this.vendorId));

    this.commService.uploadFile(form).subscribe({
      next: () => {
        this.uploading = false;
        input.value = '';
        this.loadFiles();
      },
      error: (err) => {
        this.uploading = false;
        input.value = '';
        this.fileError = err.error?.detail || 'Could not upload the file.';
        this.cdr.markForCheck();
      }
    });
  }
}
