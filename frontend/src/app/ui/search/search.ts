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
  
  @Output() search = new EventEmitter<string>();

  onInput(event: Event) {
    const input = event.target as HTMLInputElement;
    this.value = input.value;
    this.search.emit(this.value);
  }

  clear() {
    this.value = '';
    this.search.emit(this.value);
  }
}
