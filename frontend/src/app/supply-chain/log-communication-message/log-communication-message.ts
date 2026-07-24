import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

// UI Components
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';

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
export class LogCommunicationMessage {
  message = {
    poNumber: '',
    vendorName: '',
    subject: '',
    sentTime: '',
    responseTime: '',
    remarks: ''
  };

  formError: string = '';

  constructor(private router: Router) {}

  submitMessage() {
    if (!this.message.poNumber || !this.message.vendorName || !this.message.sentTime) {
      this.formError = 'Please fill in all required fields marked with an asterisk (*).';
      return;
    }

    this.formError = '';
    // Submit logic here
    console.log('Logging communication:', this.message);
    this.router.navigate(['/supply-chain/communication-tracking']);
  }

  cancel() {
    this.router.navigate(['/supply-chain/communication-tracking']);
  }
}
