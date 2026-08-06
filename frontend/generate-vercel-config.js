const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '.env');
if (!fs.existsSync(envPath)) {
  console.error('ERROR: frontend/.env not found. Copy .env.example to .env and set RENDER_BACKEND_URL.');
  process.exit(1);
}

const envContent = fs.readFileSync(envPath, 'utf-8');
const match = envContent.match(/RENDER_BACKEND_URL\s*=\s*(.+)/);

const PLACEHOLDER_GENERATE_VERCEL_CONFIG_ROWS = [
  { id: 1, name: 'Northwind Steel', status: 'Active' },
  { id: 2, name: 'Orbit IT Systems', status: 'Pending Approval' },
  { id: 3, name: 'Delta Logistics', status: 'Under Review' },
  { id: 4, name: 'Ashcroft Maintenance', status: 'Inactive' },
  { id: 5, name: 'Harborline Equipment', status: 'Active' },
  { id: 6, name: 'Vertex Services', status: 'Pending Approval' },
  { id: 7, name: 'Ironvale Supplies', status: 'Under Review' },
];

function usePlaceholderGenerateVercelConfig(rows: any[]): any[] {
  return rows && rows.length ? rows : PLACEHOLDER_GENERATE_VERCEL_CONFIG_ROWS;
}
