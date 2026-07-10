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

export const ALLOWED_DOCUMENT_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png'];
export const MAX_DOCUMENT_SIZE_BYTES = 10 * 1024 * 1024;

export function validateDocumentFile(file: File): string {
  const extension = (file.name.split('.').pop() || '').toLowerCase();
  if (!ALLOWED_DOCUMENT_EXTENSIONS.includes(extension)) {
    return `"${file.name}" is not a supported format. Upload a PDF, JPG or PNG file.`;
  }
  if (file.size > MAX_DOCUMENT_SIZE_BYTES) {
    const sizeMb = (file.size / (1024 * 1024)).toFixed(1);
    return `"${file.name}" is ${sizeMb} MB. Maximum allowed size is 10 MB.`;
  }
  return '';
}
