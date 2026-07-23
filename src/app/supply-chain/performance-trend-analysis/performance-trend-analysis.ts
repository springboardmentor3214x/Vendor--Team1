import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';

@Component({
  selector: 'app-performance-trend-analysis',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button],
  templateUrl: './performance-trend-analysis.html',
  styleUrls: ['./performance-trend-analysis.css']
})
export class PerformanceTrendAnalysis {
  vendorId: string | null = '';
  vendorName: string = 'TechCorp Solutions';

  // Mock data for trends over 6 months
  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  
  trends = [
    { label: 'Overall Reliability', data: [85, 87, 86, 90, 92, 94.5], color: '#007aff', icon: 'monitoring' },
    { label: 'Delivery Performance', data: [80, 82, 85, 88, 92, 95], color: '#34c759', icon: 'local_shipping' },
    { label: 'Product Quality', data: [90, 92, 95, 96, 97, 98], color: '#5856d6', icon: 'verified' },
    { label: 'Communication', data: [88, 88, 89, 90, 89, 90], color: '#ff9500', icon: 'forum' }
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id');
  }

  // Helper method to draw a simple SVG sparkline based on data points
  getSparklinePoints(data: number[], width: number = 300, height: number = 100): string {
    const max = 100; // max score is 100
    const min = 70;  // assuming lowest score in chart is 70 for visualization scale
    const range = max - min;
    
    const points = data.map((value, index) => {
      const x = (index / (data.length - 1)) * width;
      const y = height - (((value - min) / range) * height);
      return `${x},${y}`;
    });
    
    return points.join(' ');
  }
}
