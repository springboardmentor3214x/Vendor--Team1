import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile {

  isEditing = false;

  user = {

    fullName: 'John Doe',

    email: 'john.doe@vrip.com',

    mobile: '9876543210',

    role: localStorage.getItem('vrip_role') || 'Vendor'

  };

  editProfile() {

    this.isEditing = true;

  }

  saveProfile() {

    this.isEditing = false;

    alert('Profile Updated Successfully');

    // Backend API will be connected here later

  }

}