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
      designation: 'Manager',
      email: 'abc@gmail.com',
      phone: '9876543210',
      alternatePhone: '',
      gst: '27ABCDE1234F1Z5',
      pan: 'ABCDE1234F',
      companyRegistrationNumber: 'REG12345',
      addressLine1: '',
      addressLine2: '',
      city: '',
      state: '',
      country: '',
      pincode: '',
      website: '',
      description: '',
      bankAccountNumber: '',
      ifscCode: '',
      paymentTerms: '',
      rating: 4.8,
      status: 'Active',
      approvalStatus: 'Approved'
    },

    {
      id: 2,
      companyName: 'Delta Steel',
      category: 'Manufacturing',
      contactPerson: 'Amit Verma',
      designation: 'Owner',
      email: 'delta@gmail.com',
      phone: '9876501234',
      alternatePhone: '',
      gst: '27ABCDE5678F1Z5',
      pan: 'PQRSX5678K',
      companyRegistrationNumber: 'REG67890',
      addressLine1: '',
      addressLine2: '',
      city: '',
      state: '',
      country: '',
      pincode: '',
      website: '',
      description: '',
      bankAccountNumber: '',
      ifscCode: '',
      paymentTerms: '',
      rating: 4.2,
      status: 'Pending',
      approvalStatus: 'Pending'
    }

  ];

  private vendorSubject = new BehaviorSubject<Vendor[]>(this.vendors);

  vendors$ = this.vendorSubject.asObservable();

  getVendors(): Vendor[] {

    return this.vendors;

  }

  getVendorById(id: number): Vendor | undefined {

    return this.vendors.find(v => v.id === id);

  }

  addVendor(vendor: Vendor): void {

    vendor.id = this.vendors.length + 1;

    this.vendors.push(vendor);

    this.vendorSubject.next([...this.vendors]);

  }

  updateVendor(updatedVendor: Vendor): void {

    const index = this.vendors.findIndex(
      vendor => vendor.id === updatedVendor.id
    );

    if (index !== -1) {

      this.vendors[index] = updatedVendor;

      this.vendorSubject.next([...this.vendors]);

    }

  }

  deleteVendor(id: number): void {

    this.vendors = this.vendors.filter(
      vendor => vendor.id !== id
    );

    this.vendorSubject.next([...this.vendors]);

  }

  approveVendor(id: number): void {

    const vendor = this.vendors.find(v => v.id === id);

    if (vendor) {

      vendor.approvalStatus = 'Approved';
      vendor.status = 'Active';

      this.vendorSubject.next([...this.vendors]);

    }

  }

  rejectVendor(id: number): void {

    const vendor = this.vendors.find(v => v.id === id);

    if (vendor) {

      vendor.approvalStatus = 'Rejected';
      vendor.status = 'Rejected';

      this.vendorSubject.next([...this.vendors]);

    }

  }

  activateVendor(id: number): void {

    const vendor = this.vendors.find(v => v.id === id);

    if (vendor && vendor.approvalStatus === 'Approved') {

      vendor.status = 'Active';

      this.vendorSubject.next([...this.vendors]);

    }

  }

  suspendVendor(id: number): void {

    const vendor = this.vendors.find(v => v.id === id);

    if (vendor && vendor.approvalStatus === 'Approved') {

      vendor.status = 'Suspended';

      this.vendorSubject.next([...this.vendors]);

    }

  }

}