const fs = require('fs');
const path = require('path');

function resolveTargetUrl() {
  const possibleEnvFiles = [
    path.resolve(__dirname, '.env'),
    path.resolve(__dirname, '../backend/.env'),
    path.resolve(__dirname, '../.env')
  ];

  for (const envPath of possibleEnvFiles) {
    if (fs.existsSync(envPath)) {
      try {
        const content = fs.readFileSync(envPath, 'utf8');
        const lines = content.split(/\r?\n/);
        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
            const [key, ...valueParts] = trimmed.split('=');
            const varName = key.trim();
            const value = valueParts.join('=').trim().replace(/^["']|["']$/g, '');
            if (['BACKEND_URL', 'API_URL', 'SERVER_URL', 'PUBLIC_API_URL'].includes(varName) && value) {
              return value;
            }
          }
        }
      } catch (err) {
        // Silently fall back to process.env
      }
    }
  }

  return process.env.BACKEND_URL || process.env.API_URL || process.env.SERVER_URL || 'http://localhost:8000';
}

const targetUrl = resolveTargetUrl();

const PROXY_CONFIG = [
  {
    context: [
      "/auth",
      "/users",
      "/vendors",
      "/procurements",
      "/performance",
      "/contracts",
      "/communications"
    ],
    target: targetUrl,
    secure: false,
    changeOrigin: true,
    bypass: function (req) {
      if (req.headers && req.headers.accept && req.headers.accept.indexOf("html") !== -1) {
        return "/index.html";
      }
    }
  }
];

module.exports = PROXY_CONFIG;
