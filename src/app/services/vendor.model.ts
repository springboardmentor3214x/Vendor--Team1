export interface Vendor {

  id: number;

  companyName: string;

  category: string;

  contactPerson: string;

  email: string;

  phone: string;

  gst: string;

  rating: number;

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

}