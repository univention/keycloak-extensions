const express = require("express");
const { createProxyMiddleware, responseInterceptor } = require("http-proxy-middleware");

const {
    logger
} = require("../utils");

const { 
  getDeviceByIpOrUserAgent,
  getDeviceByCookie,
  getDeviceByFingerprintCookie 
} = require("../database");

const router = express.Router();

/**
 * @name /
 * @desc
 * Proxy everything Keycloak related
 */
router.use("/", createProxyMiddleware({
  target: process.env.KEYCLOAK_URL,
  logLevel: `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info",
  // pathFilter: "**/openid-connect/auth**",  // Micromatch
  pathFilter: "**",
  selfHandleResponse: true,
  logger: logger,
  onProxyReq: function onProxyReq(proxyReq, req, res) {
    // TODO: Check if IP block actions

    // TODO: Check if device block actions

    // TODO: Check if reCaptcha actions
    // proxyReq.setHeader('X-SUSPICIOUS-REQUEST', 1);

    // res.writeHead(429, {
    //   'Content-Type': 'text/plain',
    // });
    // res.end('Too many failed attempts. Wait for cooldown.');


    if (req.path.includes("login-actions/authenticate") && req.method === "POST") {
      const userAgent = req.headers["user-agent"];
      const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
      logger.debug(req.cookies);
      // const a = getDeviceByIpOrUserAgent(ip, userAgent);
      // const b = getDeviceByCookie(req.cookies["AUTH_SESSION_ID"]); // This is the event["code_id"]
      // const c = getDeviceByFingerprintCookie(req.cookies["DEVICE_FINGERPRINT"]);
    }
    // logger.debug(userAgent);
    // logger.debug(ip);

  },
  onProxyRes: responseInterceptor(async (responseBuffer, proxyRes, req, res) => {
      if (
      req.path.includes("openid-connect/auth") &&
      req.method === "GET" &&
      proxyRes.headers['content-type'].includes("text/html")
      ) {
      const response = responseBuffer.toString('utf8'); // Convert buffer to string
      return response + `<script>
      // Initialize the agent at application startup.
      const fpPromise = import('/fingerprintjs/v3.js')
          .then(FingerprintJS => FingerprintJS.load())

      // Get the visitor identifier when you need it.
      fpPromise
          .then(fp => fp.get())
          .then(result => {
          // This is the visitor identifier:
          const visitorId = result.visitorId
          console.log(visitorId)
          document.cookie = 'DEVICE_FINGERPRINT=' + visitorId+ ';path=/';
          })
          </script>`;
      };
      if (
        req.path.includes("login-actions/authenticate") &&
        req.method === "POST" &&
        res.statusCode === 302) {
          // TODO: notify user if new domain
          logger.debug("Login succeded, notify user if new device.")
      };
      return responseBuffer;
  }),
}));

module.exports = router;