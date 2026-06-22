import { HttpContext, HttpContextToken } from '@angular/common/http';

export const SILENT_AUTH_FAILURE = new HttpContextToken<boolean>(() => false);

export function silentRequest(): HttpContext {
  return new HttpContext().set(SILENT_AUTH_FAILURE, true);
}
