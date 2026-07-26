import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Vendor } from './vendor.model';

@Injectable({ providedIn: 'root' })
export class VendorService {
  private apiUrl = '/vendors/';
  private vendorSubject = new BehaviorSubject<Vendor[]>([]);
  vendors$ = this.vendorSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadVendors();
  }

  loadVendors(): void {
    this.http.get<any[]>(this.apiUrl).subscribe({
      next: (res) => {
        const mapped = res.map(v => ({
          ...v,
          id: v.id,
          companyName: v.company_name,
          category: v.category,
          contactPerson: v.vendor_name,
          email: v.email,
          phone: v.phone,
          status: v.status,
          approvalStatus: v.approval_status
        }));
        this.vendorSubject.next(mapped as Vendor[]);
      },
      error: () => {}
    });
  }

  getVendors(): Vendor[] {
    return this.vendorSubject.value;
  }

  getVendorById(id: number): Vendor | undefined {
    return this.vendorSubject.value.find(v => v.id === id);
  }

  addVendor(vendor: any): Observable<any> {
    const payload = {
      vendor_name: vendor.contactPerson,
      company_name: vendor.companyName,
      email: vendor.email,
      phone: vendor.phone,
      address: vendor.addressLine1 || 'N/A',
      category: vendor.category
    };
    return this.http.post<any>(this.apiUrl, payload).pipe(tap(() => this.loadVendors()));
  }

  updateVendor(updatedVendor: any): Observable<any> {
    const payload = {
      vendor_name: updatedVendor.contactPerson,
      company_name: updatedVendor.companyName,
      email: updatedVendor.email,
      phone: updatedVendor.phone,
      address: updatedVendor.addressLine1 || 'N/A',
      category: updatedVendor.category,
      status: updatedVendor.status
    };
    return this.http.put<any>(`${this.apiUrl}${updatedVendor.id}`, payload).pipe(
      tap(() => this.loadVendors())
    );
  }

  deleteVendor(id: number): void {
    this.http.delete(`${this.apiUrl}${id}`).subscribe(() => this.loadVendors());
  }

  approveVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/approve`, {}).subscribe(() => this.loadVendors());
  }

  rejectVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/reject`, {}).subscribe(() => this.loadVendors());
  }

  blockVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/block`, {}).subscribe(() => this.loadVendors());
  }

  deactivateVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/deactivate`, {}).subscribe(() => this.loadVendors());
  }

  activateVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/activate`, {}).subscribe(() => this.loadVendors());
  }

  suspendVendor(id: number): void {
    this.deactivateVendor(id);
  }
}
