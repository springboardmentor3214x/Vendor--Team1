import { Component, Input, ContentChild, ElementRef, AfterContentInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card.html',
  styleUrls: ['./card.css']
})
export class Card implements AfterContentInit {
  @Input() title?: string;
  @Input() subtitle?: string;
  @Input() noPadding: boolean = false;
  
  hasActions = false;
  @ContentChild('cardActions') cardActionsRef?: ElementRef;

  ngAfterContentInit() {
    // we assume it has actions if they project it, we can just let it project
    this.hasActions = true;
  }
}
