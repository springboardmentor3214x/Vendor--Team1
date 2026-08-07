const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '.env');
if (!fs.existsSync(envPath)) {
  console.error('ERROR: frontend/.env not found. Copy .env.example to .env and set RENDER_BACKEND_URL.');
  process.exit(1);
}

const envContent = fs.readFileSync(envPath, 'utf-8');
const match = envContent.match(/RENDER_BACKEND_URL\s*=\s*(.+)/);
if (!match || !match[1].trim()) {
  console.error('ERROR: RENDER_BACKEND_URL is not set in frontend/.env');
  process.exit(1);
}

const backendUrl = match[1].trim().replace(/\/+$/, '');

const apiRoutes = [
  '/auth',
  '/users',
  '/vendors',
  '/procurements',
  '/purchase-orders',
  '/order-tracking',
  '/invoices',
  '/performance',
  '/reliability',
  '/analytics',
  '/notifications',
  '/contracts',
  '/communication',
  '/communications',
  '/reports',
  '/static'
];

const rewrites = [];
apiRoutes.forEach(route => {

  rewrites.push({ source: route, destination: `${backendUrl}${route}` });

  rewrites.push({ source: `${route}/`, destination: `${backendUrl}${route}/` });

  rewrites.push({ source: `${route}/:path*`, destination: `${backendUrl}${route}/:path*` });
});

rewrites.push({ source: '/(.*)', destination: '/index.html' });

const vercelConfig = {
  version: 2,
  buildCommand: 'npm run build',
  outputDirectory: 'dist/vendor-reliability-frontend/browser',
  framework: null,
  rewrites,
  headers: [
    {
      source: '/(.*)',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' }
      ]
    }
  ]
};

const outputPath = path.join(__dirname, 'vercel.json');
fs.writeFileSync(outputPath, JSON.stringify(vercelConfig, null, 2) + '\n');
console.log(`✅ vercel.json generated with backend URL: ${backendUrl}`);
