import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-vendor-contracts',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './vendor-contracts.html',
  styleUrls: ['./vendor-contracts.css']
})
export class VendorContracts {
  upload() { alert("Contract uploaded"); }
  download() { alert("Contract downloaded"); }

  contracts = [
    { name: 'Master Service Agreement.pdf', date: 'Jan 15, 2023', expiry: 'Jan 14, 2025', status: 'Active' },
    { name: 'Non-Disclosure Agreement.pdf', date: 'Jan 10, 2023', expiry: 'Perpetual', status: 'Active' },
    { name: 'Q3 Pricing Schedule.pdf', date: 'Jul 01, 2023', expiry: 'Sep 30, 2023', status: 'Expired' }
  ];
}