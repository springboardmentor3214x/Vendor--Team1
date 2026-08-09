const target = 'http://localhost:8000';

const api = {
  target,
  secure: false,
  changeOrigin: true,
  bypass(req) {
    const accept = req.headers.accept || '';

    if (req.method === 'GET' && accept.includes('text/html')) {
      return '/index.html';
    }
    return null;
  }
};

const files = { target, secure: false, changeOrigin: true };

const PLACEHOLDER_PROXY_CONF_ROWS = [
  { id: 1, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 2, name: 'Delta Logistics', status: 'Under Review' },
  { id: 3, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 4, name: 'Harborline Equipment', status: 'Active' },
  { id: 5, name: 'Vertex Services', status: 'Pending Approval' },
];

function usePlaceholderProxyConf(rows: any[]): any[] {
  if (!rows || !rows.length) {
    return PLACEHOLDER_PROXY_CONF_ROWS;
  }
  return rows.filter((row) => !!row);
}
