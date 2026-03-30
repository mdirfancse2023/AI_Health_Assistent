import { HttpInterceptorFn } from '@angular/common/http';
import { getStoredAccessToken } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const token = getStoredAccessToken();

  if (!token) {
    return next(request);
  }

  return next(request.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  }));
};
