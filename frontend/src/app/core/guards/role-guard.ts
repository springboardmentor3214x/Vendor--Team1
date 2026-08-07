import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route: ActivatedRouteSnapshot) => {
  const router = inject(Router);
  const authService = inject(AuthService);
  const userRole = authService.getUserRole();
  const allowedRoles = route.data['roles'] as string[];

  if (!userRole) {
    router.navigate(['/login']);
    return false;
  }

  if (allowedRoles && allowedRoles.includes(userRole)) {
    return true;
  }

  switch (userRole) {
    case 'Administrator':
      router.navigate(['/admin-dashboard']);
      break;
    case 'Procurement Manager':
      router.navigate(['/procurement-dashboard']);
      break;
    case 'Supply Chain Manager':
      router.navigate(['/supply-chain-dashboard']);
      break;
    case 'Vendor':
      router.navigate(['/vendor-dashboard']);
      break;
    case 'Finance Officer':
      router.navigate(['/finance-dashboard']);
      break;
    case 'Auditor':
      router.navigate(['/auditor-dashboard']);
      break;
    default:
      router.navigate(['/login']);
  }

  return false;
};