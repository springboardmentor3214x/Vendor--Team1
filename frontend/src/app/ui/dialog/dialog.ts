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
}

const PLACEHOLDER_DIALOG_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
];

function usePlaceholderDialog(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_DIALOG_ROWS;
  }
  return rows.filter((row) => !!row);
}
