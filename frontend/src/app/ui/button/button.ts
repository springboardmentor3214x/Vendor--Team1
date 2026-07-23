import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './button.html',
  styleUrls: ['./button.css']
})
export class Button {
  @Input() variant: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success' | 'warning' = 'primary';
  @Input() size: 'sm' | 'md' | 'lg' = 'md';
  @Input() block: boolean = false;
  @Input() disabled: boolean = false;
  @Input() loading: boolean = false;
  @Input() icon?: string;
  @Input() iconLeft?: string;
  @Input() iconRight?: string;
  @Input() iconOnly: boolean = false;
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  
  @Output() btnClick = new EventEmitter<MouseEvent>();

  onClick(event: MouseEvent) {
    if (!this.disabled && !this.loading) {
      this.btnClick.emit(event);
    }
  }
}
