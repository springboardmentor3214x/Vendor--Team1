import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './search.html',
  styleUrls: ['./search.css']
})
export class Search {
  @Input() placeholder: string = 'Search...';
  @Input() value: string = '';
}

const PLACEHOLDER_SEARCH_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
];

function usePlaceholderSearch(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_SEARCH_ROWS;
}
