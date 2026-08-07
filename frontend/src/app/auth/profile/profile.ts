import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { InputComponent } from '../../ui/input/input';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    Card,
    Button,
    InputComponent
  ],
  templateUrl: './profile.html',
  styleUrls: ['./profile.css']
})
export class Profile implements OnInit {

  isEditing = false;

  user = {
    fullName: '',
    email: '',
    mobile: '',
    role: ''
  };

  constructor(
    private http: HttpClient,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.user.fullName = currentUser.fullName || '';
      this.user.email = currentUser.email || '';
      this.user.role = currentUser.role || this.authService.getUserRole() || '';
    }

    this.http.get<any>('/users/me').subscribe({
      next: (data) => {
        this.user.fullName = data.name || this.user.fullName;
        this.user.email    = data.email || this.user.email;
        this.user.mobile   = data.mobile_number || '';
        this.user.role     = data.role || this.user.role;
      },
      error: () => {}
    });
  }

  set fullName(val: string) {
    this.user.fullName = val;
  }

  editProfile() {
    this.isEditing = true;
  }

  saveProfile() {
    this.isEditing = false;
    alert('Profile Updated Successfully');
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}