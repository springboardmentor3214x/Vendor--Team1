import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Card } from '../../ui/card/card';
import { Button } from '../../ui/button/button';
import { NgApexchartsModule } from 'ng-apexcharts';
import { AnalyticsService } from '../../core/services/analytics.service';
import { ReliabilityService } from '../../core/services/reliability.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, Card, Button, NgApexchartsModule],
  templateUrl: './analytics.html',
  styleUrls: ['./analytics.css']
})
export class Analytics implements OnInit {
  isLoading = true;
  totalUsers = 0;
  activeUsers = 0;
  totalRoles = 6;
  totalVendors = 0;
  totalContracts = 0;
  totalProcurements = 0;
  complianceRate = 100;
  totalSpend = '₹0.00';

  public categorySpendChart: any;
  public orderStatusChart: any;
  public riskDistributionChart: any;
  public monthlyTrendChart: any;

  constructor(
    private analyticsService: AnalyticsService,
    private reliabilityService: ReliabilityService
  ) {}

  ngOnInit(): void {
    this.initCharts();
    this.loadAnalyticsData();
  }

  initCharts(): void {

    this.categorySpendChart = {
      series: [{
        name: 'Procurement Spend (₹)',
        data: []
      }],
      chart: {
        type: 'bar',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'inherit'
      },
      colors: ['#4f46e5'],
      plotOptions: {
        bar: {
          borderRadius: 6,
          columnWidth: '45%',
          distributed: true
        }
      },
      dataLabels: { enabled: false },
      xaxis: {
        categories: []
      },
      yaxis: {
        labels: {
          formatter: (val: number) => `₹${(val / 1000).toFixed(0)}k`
        }
      },
      legend: { show: false }
    };

    this.orderStatusChart = {
      series: [],
      chart: {
        type: 'donut',
        height: 320,
        fontFamily: 'inherit'
      },
      labels: ['Delivered / Completed', 'Ordered / In Transit', 'Pending Approval', 'Rejected / Cancelled'],
      colors: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
      legend: {
        position: 'bottom'
      },
      dataLabels: { enabled: true }
    };

    this.riskDistributionChart = {
      series: [],
      chart: {
        type: 'donut',
        height: 320,
        fontFamily: 'inherit'
      },
      labels: ['Low Risk (80+)', 'Medium Risk (50–79)', 'High Risk (<50)', 'Not Rated'],
      colors: ['#10b981', '#f59e0b', '#ef4444', '#94a3b8'],
      legend: {
        position: 'bottom'
      }
    };

    this.monthlyTrendChart = {
      series: [{
        name: 'Procurement Expenditure (₹)',
        data: []
      }],
      chart: {
        type: 'area',
        height: 320,
        toolbar: { show: false },
        fontFamily: 'inherit'
      },
      colors: ['#06b6d4'],
      stroke: { curve: 'smooth', width: 3 },
      fill: {
        type: 'gradient',
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.45,
          opacityTo: 0.05
        }
      },
      xaxis: {
        categories: []
      },
      yaxis: {
        labels: {
          formatter: (val: number) => `₹${(val / 1000).toFixed(0)}k`
        }
      }
    };
  }

  loadAnalyticsData(): void {
    this.isLoading = true;

    this.analyticsService.getAdminDashboard().subscribe({
      next: (data) => {
        if (data) {
          this.totalUsers = data.user_analytics?.total_users || 0;
          this.activeUsers = data.user_analytics?.active_users || 0;
          this.totalVendors = data.vendor_analytics?.total_vendors || 0;
          this.totalContracts = data.contract_analytics?.total_contracts || 0;
          this.totalProcurements = data.procurement_analytics?.total_procurement_requests || 0;
          this.complianceRate = data.compliance_analytics?.compliance_percentage || 100;
        }
      }
    });

    this.analyticsService.getProcurementManagerDashboard().subscribe({
      next: (pmData) => {
        this.isLoading = false;
        if (pmData) {
          const summary = pmData.summary || {};
          this.totalSpend = `₹${(summary.total_expenditure || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;

          if (pmData.category_breakdown && pmData.category_breakdown.length > 0) {
            const categories = pmData.category_breakdown.map((c: any) => c.category || 'General');
            const spendValues = pmData.category_breakdown.map((c: any) => c.total_spending || 0);

            this.categorySpendChart = {
              ...this.categorySpendChart,
              series: [{ name: 'Procurement Spend (₹)', data: spendValues }],
              xaxis: { categories }
            };
          }

          if (pmData.monthly_trends && pmData.monthly_trends.length > 0) {
            const months = pmData.monthly_trends.map((m: any) => m.month);
            const monthlySpend = pmData.monthly_trends.map((m: any) => m.total_spending);

            this.monthlyTrendChart = {
              ...this.monthlyTrendChart,
              series: [{ name: 'Procurement Expenditure (₹)', data: monthlySpend }],
              xaxis: { categories: months }
            };
          }

          if (summary) {
            this.orderStatusChart = {
              ...this.orderStatusChart,
              series: [
                summary.completed_orders || 0,
                summary.active_purchase_orders || 0,
                summary.pending_approvals || 0,
                summary.cancelled_orders || 0
              ]
            };
          }
        }
      },
      error: () => {
        this.isLoading = false;
      }
    });

    this.reliabilityService.getDashboard().subscribe({
      next: (relData) => {
        if (relData) {
          this.riskDistributionChart = {
            ...this.riskDistributionChart,
            series: [
              relData.high_reliability_count || 0,
              relData.medium_reliability_count || 0,
              relData.high_risk_count || 0,
              relData.not_rated_count || 0
            ]
          };
        }
      }
    });
  }

  refreshAnalytics(): void {
    this.loadAnalyticsData();
  }
}
