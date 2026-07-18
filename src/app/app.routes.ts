import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth-guard';
import { roleGuard } from './core/guards/role-guard';

import { Login } from './auth/login/login';
import { Register } from './auth/register/register';
import { ForgotPassword } from './auth/forgot-password/forgot-password';
import { Profile } from './auth/profile/profile';

import { Dashboard } from './dashboard/dashboard';

import { AdminDashboard } from './dashboard/admin-dashboard/admin-dashboard';
import { ProcurementDashboard } from './procurement/procurement-dashboard/procurement-dashboard';
import { ProcurementRequest } from './procurement/procurement-request/procurement-request';
import { ProcurementRequestList } from './procurement/procurement-request-list/procurement-request-list';
import { ProcurementApproval } from './procurement/procurement-approval/procurement-approval';
import { VendorAssignment } from './procurement/vendor-assignment/vendor-assignment';
import { PurchaseOrder } from './procurement/purchase-order/purchase-order';
import { PurchaseOrderDetails } from './procurement/purchase-order-details/purchase-order-details';
import { ProcurementStatus } from './procurement/procurement-status/procurement-status';
import { OrderTracking } from './procurement/order-tracking/order-tracking';
import { InvoiceManagement } from './procurement/invoice-management/invoice-management';
import { SupplyChainDashboard } from './dashboard/supply-chain-dashboard/supply-chain-dashboard';
import { VendorDashboard } from './dashboard/vendor-dashboard/vendor-dashboard';
import { FinanceDashboard } from './dashboard/finance-dashboard/finance-dashboard';
import { AuditorDashboard } from './dashboard/auditor-dashboard/auditor-dashboard';

import { VendorList } from './vendor/vendor-list/vendor-list';
import { AddVendor } from './vendor/add-vendor/add-vendor';
import { EditVendor } from './vendor/edit-vendor/edit-vendor';
import { VendorDetails } from './vendor/vendor-details/vendor-details';

import { UserManagement } from './admin/user-management/user-management';
import { Analytics } from './admin/analytics/analytics';
import { Reports } from './admin/reports/reports';
import { Notifications } from './admin/notifications/notifications';
import { VendorOrders } from './vendor-portal/vendor-orders/vendor-orders';
import { VendorContracts } from './vendor-portal/vendor-contracts/vendor-contracts';
import { VendorCommunication } from './vendor-portal/vendor-communication/vendor-communication';
import { VendorPerformance } from './supply-chain/vendor-performance/vendor-performance';
import { VendorPerformanceDetails } from './supply-chain/vendor-performance-details/vendor-performance-details';
import { VendorReliability } from './supply-chain/vendor-reliability/vendor-reliability';
import { DeliveryPerformance } from './supply-chain/delivery-performance/delivery-performance';
import { ProductQuality } from './supply-chain/product-quality/product-quality';
import { CommunicationTracking } from './supply-chain/communication-tracking/communication-tracking';
import { ServiceRating } from './supply-chain/service-rating/service-rating';
import { PerformanceHistory } from './supply-chain/performance-history/performance-history';
import { VendorRanking } from './supply-chain/vendor-ranking/vendor-ranking';
import { PaymentDetails } from './finance/payment-details/payment-details';
import { FinancePurchaseOrders } from './finance/finance-purchase-orders/finance-purchase-orders';
import { AuditorReports } from './auditor/auditor-reports/auditor-reports';
import { Compliance } from './auditor/compliance/compliance';
import { AuditLogs } from './auditor/audit-logs/audit-logs';
import { Settings } from './auth/settings/settings';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },

  {
    path: 'login',
    component: Login
  },

  {
    path: 'register',
    component: Register
  },

  {
    path: 'forgot-password',
    component: ForgotPassword
  },

  // -------------------- Role Dashboards --------------------

  {
    path: 'admin-dashboard',
    component: AdminDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Administrator']
    }
  },

  {
    path: 'procurement-dashboard',
    component: ProcurementDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Procurement Manager']
    }
  },

  // -------------------- Procurement Module --------------------

  {
    path: 'procurement/requests',
    component: ProcurementRequestList,
    canActivate: [authGuard]
  },

  {
    path: 'procurement-request',
    component: ProcurementRequest,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Procurement Manager']
    }
  },

  {
    path: 'procurement/approve/:id',
    component: ProcurementApproval,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Procurement Manager', 'Administrator'] }
  },

  {
    path: 'procurement/assign-vendor/:id',
    component: VendorAssignment,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Procurement Manager'] }
  },

  {
    path: 'procurement/purchase-order/create',
    component: PurchaseOrder,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Procurement Manager'] }
  },

  {
    path: 'procurement/purchase-order/:id',
    component: PurchaseOrderDetails,
    canActivate: [authGuard]
  },

  {
    path: 'procurement/status/:id',
    component: ProcurementStatus,
    canActivate: [authGuard]
  },

  {
    path: 'procurement/order-tracking/:id',
    component: OrderTracking,
    canActivate: [authGuard]
  },

  {
    path: 'procurement/invoice-management',
    component: InvoiceManagement,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['Finance Officer'] }
  },

  {
    path: 'supply-chain-dashboard',
    component: SupplyChainDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Supply Chain Manager']
    }
  },

  {
    path: 'vendor-dashboard',
    component: VendorDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Vendor']
    }
  },

  {
    path: 'finance-dashboard',
    component: FinanceDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Finance Officer']
    }
  },

  {
    path: 'auditor-dashboard',
    component: AuditorDashboard,
    canActivate: [authGuard, roleGuard],
    data: {
      roles: ['Auditor']
    }
  },

  // -------------------- Shared Dashboard --------------------

  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  },

  // -------------------- Vendor Module --------------------

  {
    path: 'vendors',
    component: VendorList,
    canActivate: [authGuard]
  },

  {
    path: 'vendors/add',
    component: AddVendor,
    canActivate: [authGuard]
  },

  {
    path: 'vendors/edit/:id',
    component: EditVendor,
    canActivate: [authGuard]
  },

  {
    path: 'vendors/:id',
    component: VendorDetails,
    canActivate: [authGuard]
  },

  // -------------------- User Profile --------------------

  {
    path: 'profile',
    component: Profile,
    canActivate: [authGuard]
  },

  // -------------------- Admin Module (New) --------------------
  { path: 'admin/user-management', component: UserManagement, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'admin/analytics', component: Analytics, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'admin/reports', component: Reports, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },
  { path: 'admin/notifications', component: Notifications, canActivate: [authGuard, roleGuard], data: { roles: ['Administrator'] } },

  // -------------------- Vendor Portal (New) --------------------
  { path: 'vendor-portal/orders', component: VendorOrders, canActivate: [authGuard, roleGuard], data: { roles: ['Vendor'] } },
  { path: 'vendor-portal/contracts', component: VendorContracts, canActivate: [authGuard, roleGuard], data: { roles: ['Vendor'] } },
  { path: 'vendor-portal/communication', component: VendorCommunication, canActivate: [authGuard, roleGuard], data: { roles: ['Vendor'] } },

  // -------------------- Supply Chain (New) --------------------
  { path: 'supply-chain/vendor-performance', component: VendorPerformance, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/delivery-performance', component: DeliveryPerformance, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/product-quality', component: ProductQuality, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/communication-tracking', component: CommunicationTracking, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/service-rating', component: ServiceRating, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/performance-history', component: PerformanceHistory, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-ranking', component: VendorRanking, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-performance/:id', component: VendorPerformanceDetails, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },
  { path: 'supply-chain/vendor-reliability', component: VendorReliability, canActivate: [authGuard, roleGuard], data: { roles: ['Supply Chain Manager'] } },

  // -------------------- Finance (New) --------------------
  { path: 'finance/payment-details', component: PaymentDetails, canActivate: [authGuard, roleGuard], data: { roles: ['Finance Officer'] } },
  { path: 'finance/purchase-orders', component: FinancePurchaseOrders, canActivate: [authGuard, roleGuard], data: { roles: ['Finance Officer'] } },

  // -------------------- Auditor (New) --------------------
  { path: 'auditor/reports', component: AuditorReports, canActivate: [authGuard, roleGuard], data: { roles: ['Auditor'] } },
  { path: 'auditor/compliance', component: Compliance, canActivate: [authGuard, roleGuard], data: { roles: ['Auditor'] } },
  { path: 'auditor/audit-logs', component: AuditLogs, canActivate: [authGuard, roleGuard], data: { roles: ['Auditor'] } },

  // -------------------- Settings --------------------
  { path: 'settings', component: Settings, canActivate: [authGuard] },

  // -------------------- Fallback --------------------

  {
    path: '**',
    redirectTo: 'login'
  }

];