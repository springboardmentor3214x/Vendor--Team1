import { Component, Input, Output, EventEmitter, TemplateRef } from '@angular/core';
import { CommonModule, NgTemplateOutlet } from '@angular/common';

export interface TableColumn {
  key: string;
  label: string;
  sortable?: boolean;
  width?: string;
  template?: TemplateRef<any>;
}

@Component({
  selector: 'app-table',
  standalone: true,
  imports: [CommonModule, NgTemplateOutlet],
  templateUrl: './table.html',
  styleUrls: ['./table.css']
})
export class Table {
  @Input() columns: TableColumn[] = [];
  @Input() data: any[] = [];
  @Input() searchable: boolean = false;
  @Input() pagination: boolean = false;
}

const PLACEHOLDER_TABLE_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderTable(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_TABLE_ROWS;
}
