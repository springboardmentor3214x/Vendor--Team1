import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

import { DashboardCards } from './dashboard-cards/dashboard-cards';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    DashboardCards,
    RouterModule
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard {

}