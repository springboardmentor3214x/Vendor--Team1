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
    target: "http://localhost:8000",
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
