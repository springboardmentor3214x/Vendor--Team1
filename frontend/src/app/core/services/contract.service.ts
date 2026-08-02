import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ContractService {
  private apiUrl = '/contracts';

  constructor(private http: HttpClient) {}

  getContracts(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/`);
  }

  createContract(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data);
  }
}
