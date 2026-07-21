import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-vendor-communication',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table, FormsModule],
  templateUrl: './vendor-communication.html',
  styleUrls: ['./vendor-communication.css']
})
export class VendorCommunication {
  newMessage = "";
  messages: any[] = [
    { sender: 'Vendor', content: 'Can we get an extension on the delivery deadline for PO-1024?', timestamp: '10:30 AM', isVendor: true },
    { sender: 'Procurement Manager', content: 'Let me check with the production team and get back to you.', timestamp: '11:15 AM', isVendor: false }
  ];
  newChat() { alert("New chat started"); }
  sendMessage() { if(this.newMessage) { this.messages.push({id: 3, sender: "You", role: "Vendor", content: this.newMessage, time: "Just now", isSelf: true }); this.newMessage = ""; } }
}