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

  deactivateVendor(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/deactivate`, {}).pipe(tap(() => this.refresh()));
  }

  activateVendor(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/activate`, {}).pipe(tap(() => this.refresh()));
  }

  suspendVendor(id: number): Observable<any> {
    return this.deactivateVendor(id);
  }

  getVendorStats(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}stats`);
  }

  uploadDocument(vendorId: number, documentType: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('document_type', documentType);
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}${vendorId}/documents`, formData);
  }

  getVendorDocuments(vendorId: number): Observable<VendorDocument[]> {
    return this.http.get<VendorDocument[]>(`${this.apiUrl}${vendorId}/documents`);
  }

  downloadDocument(vendorId: number, documentId: number): Observable<Blob> {
    return this.http.get(`${this.apiUrl}${vendorId}/documents/${documentId}/download`, {
      responseType: 'blob'
    });
  }

  deleteVendorDocument(vendorId: number, documentId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${vendorId}/documents/${documentId}`);
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
      contactPerson: vendor.contact_person || vendor.vendor_name,
      designation: vendor.designation,
      email: vendor.email,
      phone: vendor.phone,
      alternatePhone: vendor.alternate_phone,
      status: vendor.status,
      approvalStatus: vendor.approval_status,
      addressLine1: vendor.address_line_1 || vendor.address,
      addressLine2: vendor.address_line_2,
      city: vendor.city,
      state: vendor.state,
      country: vendor.country,
      pincode: vendor.pincode,
      website: vendor.website,
      description: vendor.description,
      bankAccountNumber: vendor.bank_account_number,
      ifscCode: vendor.ifsc_code,
      paymentTerms: vendor.payment_terms,
      companyRegistrationNumber: vendor.company_registration_number,
      rating: vendor.reliability_score ?? 0,
      gst: vendor.gst_number ?? '',
      pan: vendor.pan_number ?? '',
      createdBy: vendor.created_by,
      createdAt: vendor.created_at,
      updatedBy: vendor.updated_by,
      updatedAt: vendor.updated_at,
      approvedBy: vendor.approved_by,
      approvedAt: vendor.approved_at
    } as Vendor;
  }
}
