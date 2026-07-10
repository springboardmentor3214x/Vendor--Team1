import { Component } from '@angular/core';
import { Dashboard } from '../dashboard';

@Component({
  selector: 'app-vendor-dashboard',
  standalone: true,
  imports: [Dashboard],
  templateUrl: './vendor-dashboard.html',
  styleUrl: './vendor-dashboard.css'
})
export class VendorDashboard {

}