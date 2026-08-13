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

module.exports = {
  '/auth': api,
  '/users': api,
  '/vendors': api,
  '/procurements': api,
  '/purchase-orders': api,
  '/order-tracking': api,
  '/invoices': api,
  '/performance': api,
  '/reliability': api,
  '/analytics': api,
  '/notifications': api,
  '/contracts': api,
  '/communication': api,
  '/communications': api,
  '/reports': api,
  '/static': files
};
