import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router } from '@angular/router';

export const roleGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot
) => {

  const router = inject(Router);

  const userRole = localStorage.getItem('vrip_role');

  const allowedRoles = route.data['roles'] as string[];

  if (!userRole) {

    router.navigate(['/login']);

    return false;

  }

  if (allowedRoles.includes(userRole)) {

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