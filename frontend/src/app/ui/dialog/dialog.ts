import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dialog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dialog.html',
  styleUrls: ['./dialog.css']
})
export class Dialog {
  @Input() isOpen: boolean = false;
  @Input() title: string = 'Dialog';
  @Input() maxWidth: string = '500px';
}

const PLACEHOLDER_DIALOG_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderDialog(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_DIALOG_ROWS;
}
