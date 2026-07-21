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
  @Output() onClose = new EventEmitter<void>();

  close() {
    this.isOpen = false;
    this.isOpenChange.emit(this.isOpen);
    this.onClose.emit();
  }
}
