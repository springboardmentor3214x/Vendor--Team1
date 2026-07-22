import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { Table } from '../../ui/table/table';

@Component({
  selector: 'app-compliance',
  standalone: true,
  imports: [CommonModule, Card, Button, InputComponent, Table],
  templateUrl: './compliance.html',
  styleUrls: ['./compliance.css']
})
export class Compliance {
  download() { alert("Downloaded compliance document"); }

  vendors = [
    { name: 'TechCorp Solutions', category: 'IT Equipment', iso: true, gdpr: true, status: 'Compliant' },
    { name: 'Apex Suppliers Ltd.', category: 'Raw Materials', iso: false, gdpr: true, status: 'Non-Compliant' },
    { name: 'Global Parts Co.', category: 'Maintenance', iso: true, gdpr: false, status: 'Non-Compliant' },
  ];
}