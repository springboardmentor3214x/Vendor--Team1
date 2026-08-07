import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-vendor-communication',
  standalone: true,
  imports: [CommonModule, FormsModule, Card, Button],
  templateUrl: './vendor-communication.html',
  styleUrls: ['./vendor-communication.css']
})
export class VendorCommunication implements OnInit {
  messages: any[] = [];
  newMessage: string = '';
  loading: boolean = true;

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadMessages();
  }

  loadMessages(): void {
    this.loading = true;
    this.http.get<any[]>('/communications/').subscribe({
      next: (data) => {
        this.loading = false;
        if (Array.isArray(data)) {
          this.messages = data.map(m => ({
            id: m.id,
            sender: m.sender || m.sender_name || 'User',
            content: m.message || m.content || '',
            timestamp: m.sent_at ? new Date(m.sent_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now',
            isSelf: m.sender === 'Vendor' || m.sender === 'Vendor User'
          }));
        } else {
          this.messages = [];
        }
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.loading = false;
        console.error('Failed to load messages', err);
        this.cdr.markForCheck();
      }
    });
  }

  sendMessage(): void {
    if (!this.newMessage.trim()) return;
    const content = this.newMessage.trim();
    this.newMessage = '';

    const payload = {
      vendor_id: 1,
      sender: 'Vendor User',
      message: content
    };

    this.http.post('/communications/', payload).subscribe({
      next: () => this.loadMessages(),
      error: (err) => alert('Failed to send message: ' + (err.error?.detail || err.message))
    });
  }
}