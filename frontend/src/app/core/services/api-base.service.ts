import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiBaseService {
  protected base = '';

  constructor(protected http: HttpClient) {}

  list<T>(path: string): Observable<T[]> {
    return this.http.get<T[]>(`${this.base}${path}`);
  }

  single<T>(path: string): Observable<T> {
    return this.http.get<T>(`${this.base}${path}`);
  }
}
