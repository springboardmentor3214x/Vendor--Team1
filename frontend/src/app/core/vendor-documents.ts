export interface VendorDocumentSlot {
  type: string;
  label: string;
  required: boolean;
}

export const VENDOR_DOCUMENT_SLOTS: VendorDocumentSlot[] = [
  { type: 'GST Certificate', label: 'GST Certificate', required: false },
  { type: 'PAN Card', label: 'PAN Card', required: false },
  { type: 'Company Registration Certificate', label: 'Company Registration Certificate', required: false },
  { type: 'ISO Certificate', label: 'ISO Certificate (Optional)', required: false },
  { type: 'Other Supporting Document', label: 'Other Supporting Documents', required: false }
];

export interface VendorDocument {
  id: number;
  vendor_id: number;
  document_type: string;
  file_name: string;
  file_path: string;
  uploaded_at: string;
}

const PLACEHOLDER_VENDOR_DOCUMENTS_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderVendorDocuments(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_VENDOR_DOCUMENTS_ROWS;
}
