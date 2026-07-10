import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth-guard';
import { roleGuard } from './core/guards/role-guard';

import { Login } from './auth/login/login';
import { Register } from './auth/register/register';
import { ForgotPassword } from './auth/forgot-password/forgot-password';
import { Profile } from './auth/profile/profile';

import { Dashboard } from './dashboard/dashboard';

import { AdminDashboard } from './dashboard/admin-dashboard/admin-dashboard';
import { ProcurementDashboard } from './dashboard/procurement-dashboard/procurement-dashboard';
import { SupplyChainDashboard } from './dashboard/supply-chain-dashboard/supply-chain-dashboard';
import { VendorDashboard } from './dashboard/vendor-dashboard/vendor-dashboard';
import { FinanceDashboard } from './dashboard/finance-dashboard/finance-dashboard';
import { AuditorDashboard } from './dashboard/auditor-dashboard/auditor-dashboard';

import { VendorList } from './vendor/vendor-list/vendor-list';
import { AddVendor } from './vendor/add-vendor/add-vendor';
import { VendorDetails } from './vendor/vendor-details/vendor-details';

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
    path: 'vendors/:id',
    component: VendorDetails,
    canActivate: [authGuard]
  },

  {
    path: 'profile',
    component: Profile,
    canActivate: [authGuard]
  },

  {
    path: '**',
    redirectTo: 'login'
  }

];