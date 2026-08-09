export const FILE_SHARING = {

  allowedExtensions: ['pdf', 'jpg', 'jpeg', 'png', 'xls', 'xlsx', 'csv', 'doc', 'docx', 'zip'],
  maxSizeBytes: 25 * 1024 * 1024,
  acceptAttr: '.pdf,.jpg,.jpeg,.png,.xls,.xlsx,.csv,.doc,.docx,.zip',

  validate(file: File): string {
    const ext = (file.name.split('.').pop() || '').toLowerCase();
    if (!FILE_SHARING.allowedExtensions.includes(ext)) {
      return `"${file.name}" is not a supported format. Allowed: PDF, Word, Excel, CSV, images and ZIP.`;
    }
    if (file.size === 0) {
      return `"${file.name}" is empty.`;
    }
    if (file.size > FILE_SHARING.maxSizeBytes) {
      return `"${file.name}" is ${(file.size / (1024 * 1024)).toFixed(1)} MB. Maximum allowed size is 25 MB.`;
    }
    return '';
  },

  formatSize(bytes?: number | null): string {
    if (bytes === null || bytes === undefined || bytes <= 0) return '—';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  },

  iconFor(fileName?: string | null): string {
    const ext = (fileName?.split('.').pop() || '').toLowerCase();
    if (ext === 'pdf') return 'picture_as_pdf';
    if (['xls', 'xlsx', 'csv'].includes(ext)) return 'table_view';
    if (['doc', 'docx'].includes(ext)) return 'description';
    if (['jpg', 'jpeg', 'png'].includes(ext)) return 'image';
    if (ext === 'zip') return 'folder_zip';
    return 'draft';
  },

  saveBlob(blob: Blob, fileName: string): void {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName || 'download';
    a.click();
    window.URL.revokeObjectURL(url);
  }
};
