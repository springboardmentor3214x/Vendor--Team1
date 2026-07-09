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
}

const PLACEHOLDER_VENDOR_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendor(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_ROWS;
}
