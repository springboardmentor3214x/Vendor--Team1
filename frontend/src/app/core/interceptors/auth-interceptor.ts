import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const token = localStorage.getItem('vrip_token');
  if (token) {
    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }
  return next(req).pipe(
    catchError(err => {
      if (err.status === 401) {
        localStorage.removeItem('vrip_token');
        localStorage.removeItem('vrip_role');
        localStorage.removeItem('vrip_user');
        router.navigate(['/login']);
      }
      return throwError(() => err);
    })
  );
};
