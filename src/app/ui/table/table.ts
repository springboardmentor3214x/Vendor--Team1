import { Component, Input, Output, EventEmitter, TemplateRef } from '@angular/core';
import { CommonModule } from '@angular/common';

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
  imports: [CommonModule],
  templateUrl: './table.html',
  styleUrls: ['./table.css']
})
export class Table {
  @Input() columns: TableColumn[] = [];
  @Input() data: any[] = [];
  @Input() searchable: boolean = false;
  @Input() pagination: boolean = false;
  @Input() totalItems: number = 0;
  @Input() hasToolbar: boolean = false;
  @Input() hasActionsCol: boolean = false;

  @Output() search = new EventEmitter<string>();

  onSearch(event: Event) {
    const input = event.target as HTMLInputElement;
    this.search.emit(input.value);
  }
}
