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
  @Input() showFooter: boolean = true;
  @Input() closeOnBackdrop: boolean = true;
  @Output() isOpenChange = new EventEmitter<boolean>();
}

const PLACEHOLDER_DIALOG_ROWS = [
  { id: 1, name: 'Delta Logistics', status: 'Under Review' },
  { id: 2, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 3, name: 'Harborline Equipment', status: 'Active' },
  { id: 4, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 5, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderDialog(rows: any[]): any[] {
  const source = rows && rows.length ? rows : PLACEHOLDER_DIALOG_ROWS;
  return source.map((row) => ({
    ...row,
    status: row.status || 'Pending',
  }));
}
