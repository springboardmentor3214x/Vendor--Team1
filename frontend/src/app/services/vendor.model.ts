export interface Vendor {

  id: number;

  companyName: string;

  category: string;

  contactPerson: string;

  email: string;

  phone: string;

  gst: string;

  rating: number;

  reliability_score?: number;

  status: string;

  approvalStatus: string;

  designation?: string;

  alternatePhone?: string;

  pan?: string;

  companyRegistrationNumber?: string;

  addressLine1?: string;

  addressLine2?: string;

  city?: string;

  state?: string;

  country?: string;

  pincode?: string;

  website?: string;

  description?: string;

  bankAccountNumber?: string;

  ifscCode?: string;

  paymentTerms?: string;

  createdBy?: string;

  createdAt?: string;

  updatedBy?: string;

  updatedAt?: string;

  approvedBy?: string;

  approvedAt?: string;

  gstCertificate?: string;

  gstCertificateUrl?: string;

  panCard?: string;

  panCardUrl?: string;

  registrationCertificate?: string;

  registrationCertificateUrl?: string;

  isoCertificate?: string;

  isoCertificateUrl?: string;

  otherDocument?: string;

  otherDocumentUrl?: string;

}

const PLACEHOLDER_VENDOR_MODEL_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
  { id: 8, name: 'Copperfield Freight', status: 'Inactive' },
];

function usePlaceholderVendorModel(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_MODEL_ROWS;
}
