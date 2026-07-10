import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Vendor } from './vendor.model';

@Injectable({
  providedIn: 'root'
})
export class VendorService {

  private vendors: Vendor[] = [

    {
      id: 1,
      companyName: 'ABC Pvt Ltd',
      category: 'Electronics',
      contactPerson: 'Rahul Sharma',
      email: 'abc@gmail.com',
      phone: '9876543210',
      gst: '27ABCDE1234F1Z5',
      rating: 4.8,
      status: 'Active',
      approvalStatus: 'Approved'
    },

    {
      id: 2,
      companyName: 'Delta Steel',
      category: 'Manufacturing',
      contactPerson: 'Priya Verma',
      email: 'delta@gmail.com',
      phone: '9876501234',
      gst: '27ABCDE5678F1Z5',
      rating: 4.2,
      status: 'Pending',
      approvalStatus: 'Pending'
    }

  ];

  private vendorSubject = new BehaviorSubject<Vendor[]>(this.vendors);

  vendors$ = this.vendorSubject.asObservable();

  getVendors(): Vendor[] {

    return this.vendorSubject.value;

  }

  addVendor(vendor: Vendor): void {

    vendor.id = this.vendors.length + 1;

    this.vendors.push(vendor);

    this.vendorSubject.next(this.vendors);

  }

  updateVendor(updatedVendor: Vendor): void {

    const index = this.vendors.findIndex(v => v.id === updatedVendor.id);

    if (index !== -1) {

      this.vendors[index] = updatedVendor;

      this.vendorSubject.next(this.vendors);

    }

  }

  deleteVendor(id: number): void {

    this.vendors = this.vendors.filter(v => v.id !== id);

    this.vendorSubject.next(this.vendors);

  }

}