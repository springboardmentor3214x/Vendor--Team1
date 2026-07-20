import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-badge',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './badge.html',
  styleUrls: ['./badge.css']
})
export class Badge {
  @Input() variant: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info' = 'default';
  @Input() size: 'sm' | 'md' | 'lg' = 'md';
  @Input() icon?: string;
}
