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

const PLACEHOLDER_PROXY_CONF_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
];

function usePlaceholderProxyConf(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_PROXY_CONF_ROWS;
}
