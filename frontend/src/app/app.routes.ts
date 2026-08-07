import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth-guard';
import { roleGuard } from './core/guards/role-guard';

const page = {
  Login: () => import('./auth/login/login').then(m => m.Login),
  Register: () => import('./auth/register/register').then(m => m.Register),
  ForgotPassword: () => import('./auth/forgot-password/forgot-password').then(m => m.ForgotPassword),
  Profile: () => import('./auth/profile/profile').then(m => m.Profile),
  Dashboard: () => import('./dashboard/dashboard').then(m => m.Dashboard),
  AdminDashboard: () => import('./dashboard/admin-dashboard/admin-dashboard').then(m => m.AdminDashboard),
  ProcurementDashboard: () => import('./procurement/procurement-dashboard/procurement-dashboard').then(m => m.ProcurementDashboard),
  ProcurementRequest: () => import('./procurement/procurement-request/procurement-request').then(m => m.ProcurementRequest),
  ProcurementRequestList: () => import('./procurement/procurement-request-list/procurement-request-list').then(m => m.ProcurementRequestList),
  ProcurementApproval: () => import('./procurement/procurement-approval/procurement-approval').then(m => m.ProcurementApproval),
  VendorAssignment: () => import('./procurement/vendor-assignment/vendor-assignment').then(m => m.VendorAssignment),
  PurchaseOrder: () => import('./procurement/purchase-order/purchase-order').then(m => m.PurchaseOrder),
  PurchaseOrderDetails: () => import('./procurement/purchase-order-details/purchase-order-details').then(m => m.PurchaseOrderDetails),
  ProcurementStatus: () => import('./procurement/procurement-status/procurement-status').then(m => m.ProcurementStatus),
  OrderTracking: () => import('./procurement/order-tracking/order-tracking').then(m => m.OrderTracking),
  InvoiceManagement: () => import('./procurement/invoice-management/invoice-management').then(m => m.InvoiceManagement),
  SupplyChainDashboard: () => import('./dashboard/supply-chain-dashboard/supply-chain-dashboard').then(m => m.SupplyChainDashboard),
  VendorDashboard: () => import('./dashboard/vendor-dashboard/vendor-dashboard').then(m => m.VendorDashboard),
  FinanceDashboard: () => import('./dashboard/finance-dashboard/finance-dashboard').then(m => m.FinanceDashboard),
  AuditorDashboard: () => import('./dashboard/auditor-dashboard/auditor-dashboard').then(m => m.AuditorDashboard),
  VendorList: () => import('./vendor/vendor-list/vendor-list').then(m => m.VendorList),
  AddVendor: () => import('./vendor/add-vendor/add-vendor').then(m => m.AddVendor),
  EditVendor: () => import('./vendor/edit-vendor/edit-vendor').then(m => m.EditVendor),
  VendorDetails: () => import('./vendor/vendor-details/vendor-details').then(m => m.VendorDetails),
  UserManagement: () => import('./admin/user-management/user-management').then(m => m.UserManagement),
  Analytics: () => import('./admin/analytics/analytics').then(m => m.Analytics),
  Reports: () => import('./admin/reports/reports').then(m => m.Reports),
  Notifications: () => import('./admin/notifications/notifications').then(m => m.Notifications),
  VendorOrders: () => import('./vendor-portal/vendor-orders/vendor-orders').then(m => m.VendorOrders),
  VendorContracts: () => import('./vendor-portal/vendor-contracts/vendor-contracts').then(m => m.VendorContracts),
  VendorCommunication: () => import('./vendor-portal/vendor-communication/vendor-communication').then(m => m.VendorCommunication),
  VendorPerformance: () => import('./supply-chain/vendor-performance/vendor-performance').then(m => m.VendorPerformance),
  VendorPerformanceDetails: () => import('./supply-chain/vendor-performance-details/vendor-performance-details').then(m => m.VendorPerformanceDetails),
  VendorReliability: () => import('./supply-chain/vendor-reliability/vendor-reliability').then(m => m.VendorReliability),
  VendorReliabilityDashboard: () => import('./supply-chain/vendor-reliability-dashboard/vendor-reliability-dashboard').then(m => m.VendorReliabilityDashboard),
  ReliabilityScoreDetails: () => import('./supply-chain/reliability-score-details/reliability-score-details').then(m => m.ReliabilityScoreDetails),
  ProcurementRiskDashboard: () => import('./supply-chain/procurement-risk-dashboard/procurement-risk-dashboard').then(m => m.ProcurementRiskDashboard),
  PerformanceTrendAnalysis: () => import('./supply-chain/performance-trend-analysis/performance-trend-analysis').then(m => m.PerformanceTrendAnalysis),
  ProcurementRecommendations: () => import('./supply-chain/procurement-recommendations/procurement-recommendations').then(m => m.ProcurementRecommendations),
  DeliveryPerformance: () => import('./supply-chain/delivery-performance/delivery-performance').then(m => m.DeliveryPerformance),
  ProductQuality: () => import('./supply-chain/product-quality/product-quality').then(m => m.ProductQuality),
  CommunicationTracking: () => import('./supply-chain/communication-tracking/communication-tracking').then(m => m.CommunicationTracking),
  ServiceRating: () => import('./supply-chain/service-rating/service-rating').then(m => m.ServiceRating),
  PerformanceHistory: () => import('./supply-chain/performance-history/performance-history').then(m => m.PerformanceHistory),
  VendorRanking: () => import('./supply-chain/vendor-ranking/vendor-ranking').then(m => m.VendorRanking),
  PaymentDetails: () => import('./finance/payment-details/payment-details').then(m => m.PaymentDetails),
  FinancePurchaseOrders: () => import('./finance/finance-purchase-orders/finance-purchase-orders').then(m => m.FinancePurchaseOrders),
  AuditorReports: () => import('./auditor/auditor-reports/auditor-reports').then(m => m.AuditorReports),
  Compliance: () => import('./auditor/compliance/compliance').then(m => m.Compliance),
  AuditLogs: () => import('./auditor/audit-logs/audit-logs').then(m => m.AuditLogs),
  Settings: () => import('./auth/settings/settings').then(m => m.Settings),
  NewProductEvaluation: () => import('./supply-chain/new-product-evaluation/new-product-evaluation').then(m => m.NewProductEvaluation),
  LogCommunicationMessage: () => import('./supply-chain/log-communication-message/log-communication-message').then(m => m.LogCommunicationMessage),
  SubmitServiceRating: () => import('./supply-chain/submit-service-rating/submit-service-rating').then(m => m.SubmitServiceRating),
};

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: page.Login
  },
  {
    path: 'register',
    loadComponent: page.Register
  },
  {
    path: 'forgot-password',
    loadComponent: page.ForgotPassword
  },
  {
    path: 'admin-dashboard',
    loadComponent: page.AdminDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Administrator']
    }
  },
  {
    path: 'procurement-dashboard',
    loadComponent: page.ProcurementDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Procurement Manager']
    }
  },
  {
    path: 'procurement/requests',
    loadComponent: page.ProcurementRequestList,
    canActivate: [authGuard]
  },
  {
    path: 'procurement-request',
    loadComponent: page.ProcurementRequest,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Procurement Manager', 'Supply Chain Manager']
    }
  },
  {
    path: 'procurement/approve/:id',
    loadComponent: page.ProcurementApproval,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Procurement Manager', 'Administrator'] }
  },
  {
    path: 'procurement/assign-vendor/:id',
    loadComponent: page.VendorAssignment,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Procurement Manager'] }
  },
  {
    path: 'procurement/purchase-order/create',
    loadComponent: page.PurchaseOrder,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Procurement Manager'] }
  },
  {
    path: 'procurement/purchase-order/:id',
    loadComponent: page.PurchaseOrderDetails,
    canActivate: [authGuard]
  },
  {
    path: 'procurement/status/:id',
    loadComponent: page.ProcurementStatus,
    canActivate: [authGuard]
  },
  {
    path: 'procurement/order-tracking/:id',
    loadComponent: page.OrderTracking,
    canActivate: [authGuard]
  },
  {
    path: 'procurement/invoice-management',
    loadComponent: page.InvoiceManagement,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Finance Officer', 'Procurement Manager'] }
  },
  {
    path: 'supply-chain-dashboard',
    loadComponent: page.SupplyChainDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Supply Chain Manager']
    }
  },
  {
    path: 'vendor-dashboard',
    loadComponent: page.VendorDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Vendor']
    }
  },
  {
    path: 'finance-dashboard',
    loadComponent: page.FinanceDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Finance Officer']
    }
  },
  {
    path: 'auditor-dashboard',
    loadComponent: page.AuditorDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Auditor']
    }
  },
  {
    path: 'dashboard',
    loadComponent: page.Dashboard,
    canActivate: [authGuard]
  },
  {
    path: 'vendors',
    loadComponent: page.VendorList,
    canActivate: [authGuard]
  },
  {
    path: 'vendors/add',
    loadComponent: page.AddVendor,
    canActivate: [authGuard]
  },
  {
    path: 'vendors/edit/:id',
    loadComponent: page.EditVendor,
    canActivate: [authGuard]
  },
  {
    path: 'vendors/:id',
    loadComponent: page.VendorDetails,
    canActivate: [authGuard]
  },
  {
    path: 'profile',
    loadComponent: page.Profile,
    canActivate: [authGuard]
  },
  { path: 'admin/user-management', loadComponent: page.UserManagement, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'admin/analytics', loadComponent: page.Analytics, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'admin/reports', loadComponent: page.Reports, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'admin/notifications', loadComponent: page.Notifications, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'vendor-portal/orders', loadComponent: page.VendorOrders, canActivate: [authGuard, roleGuard], data: { roles: ['Vendor'] } },
  { path: 'vendor-portal/contracts', loadComponent: page.VendorContracts, canActivate: [authGuard, roleGuard], data: { roles: ['Vendor'] } },
  { path: 'vendor-portal/communication', loadComponent: page.VendorCommunication, canActivate: [authGuard, roleGuard], data: { roles: ['Vendor'] } },
  { path: 'supply-chain/vendor-performance', loadComponent: page.VendorPerformance, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/delivery-performance', loadComponent: page.DeliveryPerformance, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/product-quality', loadComponent: page.ProductQuality, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/product-quality/new', loadComponent: page.NewProductEvaluation, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/communication-tracking', loadComponent: page.CommunicationTracking, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/communication-tracking/new', loadComponent: page.LogCommunicationMessage, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/service-rating', loadComponent: page.ServiceRating, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/service-rating/new', loadComponent: page.SubmitServiceRating, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/performance-history', loadComponent: page.PerformanceHistory, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-ranking', loadComponent: page.VendorRanking, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-performance/:id', loadComponent: page.VendorPerformanceDetails, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-reliability', loadComponent: page.VendorReliability, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-reliability-dashboard', loadComponent: page.VendorReliabilityDashboard, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/reliability-score-details/:id', loadComponent: page.ReliabilityScoreDetails, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/procurement-risk-dashboard', loadComponent: page.ProcurementRiskDashboard, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/performance-trend-analysis/:id', loadComponent: page.PerformanceTrendAnalysis, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/procurement-recommendations', loadComponent: page.ProcurementRecommendations, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'finance/payment-details', loadComponent: page.PaymentDetails, canActivate: [authGuard, roleGuard], data: { roles: ['Finance Officer'] } },
  { path: 'finance/purchase-orders', loadComponent: page.FinancePurchaseOrders, canActivate: [authGuard, roleGuard], data: { roles: ['Finance Officer'] } },
  { path: 'auditor/reports', loadComponent: page.AuditorReports, canActivate: [authGuard, roleGuard], data: { roles: ['Auditor'] } },
  { path: 'auditor/compliance', loadComponent: page.Compliance, canActivate: [authGuard, roleGuard], data: { roles: ['Auditor'] } },
  { path: 'auditor/audit-logs', loadComponent: page.AuditLogs, canActivate: [authGuard, roleGuard], data: { roles: ['Auditor'] } },
  { path: 'settings', loadComponent: page.Settings, canActivate: [authGuard] },
  {
    path: '**',
    redirectTo: 'login'
  }
];
