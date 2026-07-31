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

  constructor(
    private router: Router,
    private commService: CommunicationService
  ) {}

  ngOnInit(): void {

    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    this.message.sentTime = now.toISOString().slice(0, 16);
  }

  submitMessage() {
    if (!this.message.poNumber || !this.message.vendorName) {
      this.formError = 'Please fill in PO Number and Vendor Name.';
      return;
    }

    if (!this.message.sentTime) {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      this.message.sentTime = now.toISOString().slice(0, 16);
    }

    this.formError = '';
    const payload = {
      message: `${this.message.subject || 'Communication Log'} [PO: ${this.message.poNumber}]`,
      sender_name: 'Procurement Manager',
      remarks: this.message.remarks
    };

    this.commService.sendMessage(payload).subscribe({
      next: () => {
        this.router.navigate(['/supply-chain/communication-tracking']);
      },
      error: (err) => {
        console.warn('API log created or fallback redirecting...', err);
        this.router.navigate(['/supply-chain/communication-tracking']);
      }
    });
  }

  cancel() {
    this.router.navigate(['/supply-chain/communication-tracking']);
  }
}
