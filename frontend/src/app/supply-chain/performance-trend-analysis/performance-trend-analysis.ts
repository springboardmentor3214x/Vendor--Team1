import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-performance-trend-analysis',
  standalone: true,
  imports: [CommonModule, RouterModule, Card, Button],
  templateUrl: './performance-trend-analysis.html',
  styleUrls: ['./performance-trend-analysis.css']
})
export class PerformanceTrendAnalysis implements OnInit {
  vendorId: string | null = '';
  vendorName: string = 'Loading…';
  isLoading = true;
  errorMsg = '';

  months: string[] = [];
  overallTrend = '';
  currentScore: number | null = null;

  trends: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private reliabilityService: ReliabilityService
  ) {}

  ngOnInit() {
    this.vendorId = this.route.snapshot.paramMap.get('id') || '1';
    this.loadTrends(this.vendorId);
  }

  loadTrends(id: string) {
    this.isLoading = true;
    this.reliabilityService.getTrends(id).subscribe({
      next: (res) => {
        this.isLoading = false;
        if (res && res.monthly_trends) {
          this.vendorName = res.company_name || res.vendor_name;
          this.overallTrend = res.overall_trend || '';
          this.currentScore = res.current_reliability_score ?? null;

          const pts = res.monthly_trends;
          this.months = pts.map((p: any) => p.period);

          this.trends = [
            { label: 'Overall Reliability', data: pts.map((p: any) => p.reliability_score), color: '#007aff', icon: 'monitoring' },
            { label: 'Delivery Performance', data: pts.map((p: any) => p.delivery_score), color: '#34c759', icon: 'local_shipping' },
            { label: 'Product Quality', data: pts.map((p: any) => p.quality_score), color: '#5856d6', icon: 'verified' },
            { label: 'Communication', data: pts.map((p: any) => p.communication_score), color: '#ff9500', icon: 'forum' },
            { label: 'Service Rating', data: pts.map((p: any) => p.service_score), color: '#af52de', icon: 'star_rate' }
          ];

          if (pts.length === 0) {
            this.errorMsg = 'This vendor has no dated performance records yet, so no trend can be shown.';
          }
        }
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = err.error?.detail || 'Could not load the performance trend.';
      }
    });
  }

  getSparklinePoints(data: (number | null)[], width: number = 300, height: number = 100): string {
    if (!data || data.length === 0) {
      return '';
    }

    const divisor = data.length > 1 ? data.length - 1 : 1;

    return data
      .map((value, index) => ({ value, index }))
      .filter(p => p.value !== null && p.value !== undefined && !isNaN(p.value as number))
      .map(p => {
        const x = (p.index / divisor) * width;
        const y = height - ((p.value as number) / 100) * height;
        return `${x},${y}`;
      })
      .join(' ');
  }

  hasData(data: (number | null)[]): boolean {
    return (data || []).some(v => v !== null && v !== undefined);
  }

  private measured(data: (number | null)[]): number[] {
    return (data || []).filter(v => v !== null && v !== undefined) as number[];
  }

  latestScore(data: (number | null)[]): string {
    const values = this.measured(data);
    return values.length ? values[values.length - 1].toFixed(1) : '—';
  }

  change(data: (number | null)[]): number | null {
    const values = this.measured(data);
    return values.length >= 2 ? values[values.length - 1] - values[0] : null;
  }

  changeLabel(data: (number | null)[]): string {
    const delta = this.change(data);
    if (delta === null) {
      return '—';
    }
    return `${delta >= 0 ? '+' : ''}${delta.toFixed(1)}%`;
  }

  changeColor(data: (number | null)[]): string {
    const delta = this.change(data);
    if (delta === null) {
      return 'var(--text-secondary)';
    }
    return delta >= 0 ? '#34c759' : '#ff3b30';
  }
}
