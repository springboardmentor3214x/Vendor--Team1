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

  getExpiringContracts(days: number = 90): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/expiring?days=${days}`);
  }

  getContractById(id: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  createContract(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/`, data);
  }

  createContractWithFile(formData: FormData): Observable<any> {
    return this.http.post(`${this.apiUrl}/upload`, formData);
  }

  updateContract(id: string | number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }

  renewContract(id: string | number, newEndDate: string, newValue?: number): Observable<any> {
    const url = newValue 
      ? `${this.apiUrl}/${id}/renew?new_end_date=${newEndDate}&new_value=${newValue}`
      : `${this.apiUrl}/${id}/renew?new_end_date=${newEndDate}`;
    return this.http.post(url, {});
  }

  deleteContract(id: string | number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  // Certifications
  addCertification(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/certifications`, data);
  }

  getVendorCertifications(vendorId: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/certifications/${vendorId}`);
  }

  deleteCertification(certId: string | number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/certifications/${certId}`);
  }

  // Compliance
  recordCompliance(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/compliance`, data);
  }

  getVendorCompliance(vendorId: string | number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/compliance/${vendorId}`);
  }

  updateComplianceStatus(id: string | number, status: string, remarks?: string): Observable<any> {
    const url = remarks 
      ? `${this.apiUrl}/compliance/${id}?status=${status}&remarks=${encodeURIComponent(remarks)}`
      : `${this.apiUrl}/compliance/${id}?status=${status}`;
    return this.http.put(url, {});
  }

  getComplianceDashboard(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/compliance/dashboard`);
  }
}
