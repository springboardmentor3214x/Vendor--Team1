import { Component } from '@angular/core';
import { Dashboard } from '../dashboard';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [Dashboard],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.css'
})
export class AdminDashboard {


  refresh() { alert("Data refreshed!"); }
}