import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css'
})
export class Sidebar {

  role: string = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {
    this.role = localStorage.getItem('vrip_role') || '';
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}