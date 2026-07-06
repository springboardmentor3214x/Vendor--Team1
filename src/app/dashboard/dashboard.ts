import { Component } from '@angular/core';
import { DashboardCards } from './dashboard-cards/dashboard-cards';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DashboardCards],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard {

}