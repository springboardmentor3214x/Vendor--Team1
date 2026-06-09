import { HttpContext, HttpContextToken } from '@angular/common/http';

export const SILENT_AUTH_FAILURE = new HttpContextToken<boolean>(() => false);
