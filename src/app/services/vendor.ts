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
      name: 'ABC Pvt Ltd',
      category: 'Electronics',
      email: 'abc@gmail.com',
      phone: '9876543210',
      gst: '27ABCDE1234F1Z5',
      rating: 4.8,
      status: 'Approved'
    },

    {
      id: 2,
      name: 'Delta Steel',
      category: 'Manufacturing',
      email: 'delta@gmail.com',
      phone: '9876501234',
      gst: '27ABCDE5678F1Z5',
      rating: 4.2,
      status: 'Pending'
    }

  ];

  private vendorSubject = new BehaviorSubject<Vendor[]>(this.vendors);

  vendors$ = this.vendorSubject.asObservable();

  getVendors() {

    return this.vendorSubject.value;

  }

  addVendor(vendor: Vendor) {

    vendor.id = this.vendors.length + 1;

    this.vendors.push(vendor);

    this.vendorSubject.next(this.vendors);

  }

}