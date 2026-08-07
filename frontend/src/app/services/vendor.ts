import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Vendor } from './vendor.model';

@Injectable({ providedIn: 'root' })
export class VendorService {
  private apiUrl = '/vendors/';
  private vendorSubject = new BehaviorSubject<Vendor[]>([]);
  readonly vendors$ = this.vendorSubject.asObservable();

  constructor(private http: HttpClient) {}

  loadVendors(): Observable<Vendor[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map((vendors) => vendors.map((vendor) => this.mapVendor(vendor))),
      tap((vendors) => this.vendorSubject.next(vendors)),
      catchError((error) => {
        console.error('Failed to load vendors', error);
        return throwError(() => error);
      })
    );
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
    return this.http.post<any>(this.apiUrl, payload).pipe(tap(() => this.refresh()));
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
      tap(() => this.refresh())
    );
  }

  deleteVendor(id: number): void {
    this.http.delete(`${this.apiUrl}${id}`).subscribe(() => this.refresh());
  }

  approveVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/approve`, {}).subscribe(() => this.refresh());
  }

  rejectVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/reject`, {}).subscribe(() => this.refresh());
  }

  blockVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/block`, {}).subscribe(() => this.refresh());
  }

  deactivateVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/deactivate`, {}).subscribe(() => this.refresh());
  }

  activateVendor(id: number): void {
    this.http.post(`${this.apiUrl}${id}/activate`, {}).subscribe(() => this.refresh());
  }

  suspendVendor(id: number): void {
    this.deactivateVendor(id);
  }

  private refresh(): void {
    this.loadVendors().subscribe({ error: () => undefined });
  }

  private mapVendor(vendor: any): Vendor {
    return {
      ...vendor,
      id: vendor.id,
      companyName: vendor.company_name,
      category: vendor.category,
      contactPerson: vendor.vendor_name,
      email: vendor.email,
      phone: vendor.phone,
      status: vendor.status,
      approvalStatus: vendor.approval_status,
      addressLine1: vendor.address,
      rating: vendor.reliability_score ?? 0,
      gst: vendor.gst ?? ''
    } as Vendor;
  }
}
