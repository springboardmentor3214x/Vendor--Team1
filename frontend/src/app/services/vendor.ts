import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Vendor } from './vendor.model';
import { VendorDocument } from '../core/vendor-documents';

@Injectable({ providedIn: 'root' })
export class VendorService {
  private apiUrl = '/vendors/';
  private vendorSubject = new BehaviorSubject<Vendor[]>([]);
  readonly vendors$ = this.vendorSubject.asObservable();
  constructor(private http: HttpClient) {}
  loadVendors(): Observable<Vendor[]> {

    return this.http.get<any[]>(`${this.apiUrl}?limit=1000`).pipe(
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
  getMyVendorProfile(): Observable<Vendor> {
    return this.http.get<any>(`${this.apiUrl}me`).pipe(
      map((vendor) => this.mapVendor(vendor))
    );
  }
  getVendorById(id: number): Vendor | undefined {
    return this.vendorSubject.value.find(v => v.id === id);
  }
  private toPayload(vendor: any): any {
    const fullAddress = [
      vendor.addressLine1, vendor.addressLine2, vendor.city, vendor.state, vendor.pincode
    ].filter(Boolean).join(', ');

    return {
      vendor_name: vendor.contactPerson,
      company_name: vendor.companyName,
      email: vendor.email,
      phone: vendor.phone,
      address: fullAddress || vendor.addressLine1 || 'N/A',
      category: vendor.category,
      contact_person: vendor.contactPerson,
      designation: vendor.designation || null,
      alternate_phone: vendor.alternatePhone || null,
      gst_number: vendor.gst || null,
      pan_number: vendor.pan || null,
      company_registration_number: vendor.companyRegistrationNumber || null,
      address_line_1: vendor.addressLine1 || null,
      address_line_2: vendor.addressLine2 || null,
      city: vendor.city || null,
      state: vendor.state || null,
      country: vendor.country || null,
      pincode: vendor.pincode || null,
      website: vendor.website || null,
      description: vendor.description || null,
      bank_account_number: vendor.bankAccountNumber || null,
      ifsc_code: vendor.ifscCode || null,
      payment_terms: vendor.paymentTerms || null
    };
  }
  addVendor(vendor: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, this.toPayload(vendor)).pipe(tap(() => this.refresh()));
  }
  updateVendor(updatedVendor: any): Observable<any> {
    const payload = { ...this.toPayload(updatedVendor), status: updatedVendor.status };
    return this.http.put<any>(`${this.apiUrl}${updatedVendor.id}`, payload).pipe(
      tap(() => this.refresh())
    );
  }
  deleteVendor(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}`).pipe(tap(() => this.refresh()));
  }
  approveVendor(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/approve`, {}).pipe(tap(() => this.refresh()));
  }
  rejectVendor(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/reject`, {}).pipe(tap(() => this.refresh()));
  }
  blockVendor(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/block`, {}).pipe(tap(() => this.refresh()));
  }
}

const PLACEHOLDER_VENDOR_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 6, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 7, name: 'Copperfield Freight', status: 'Inactive' },
  { id: 8, name: 'Northwind Steel', status: 'Active' },
];

function usePlaceholderVendor(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_VENDOR_ROWS;
  }
  return rows.filter((row) => !!row);
}
