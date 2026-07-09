import { Routes } from '@angular/router';

import { Dashboard } from './dashboard/dashboard';
import { Login } from './auth/login/login';
import { Register } from './auth/register/register';
import { ForgotPassword } from './auth/forgot-password/forgot-password';
import { Profile } from './auth/profile/profile';
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

  {
    path: 'dashboard',
    component: Dashboard
  },

  {
    path: 'vendors',
    component: VendorList
  },

  {
    path: 'vendors/add',
    component: AddVendor
  },

  {
    path: 'vendors/:id',
    component: VendorDetails
  },

  {
    path: 'profile',
    component: Profile
  },

  {
    path: '**',
    redirectTo: 'login'
  }

];