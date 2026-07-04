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
  @Input() totalItems: number = 0;
  @Input() hasToolbar: boolean = false;
  @Input() hasActionsCol: boolean = false;
  @Input() loading: boolean = false;
  @Input() skeletonRows: number = 4;

  @Output() search = new EventEmitter<string>();

  get dummyRows(): number[] {
    return Array.from({ length: this.skeletonRows });
  }

  onSearch(event: Event) {
    const input = event.target as HTMLInputElement;
    this.search.emit(input.value);
  }
}
