const express = require("express");
const { createProxyMiddleware, responseInterceptor } = require("http-proxy-middleware");

const {
    logger
} = require("../utils");

const { 
  getDeviceByIpOrUserAgent,
  getDeviceByCookie,
  getDeviceByFingerprintCookie,
  getActionsForIP,
  getActionsForDevice,
} = require("../database");

const router = express.Router();


// FIXME: Not clean, but workaround for:
// https://github.com/chimurai/http-proxy-middleware/issues/318
const fetchBlockActions = async (req, res, next) => {
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  req._ipBlockActions = await getActionsForIP(ip, "ip");
  req._deviceBlockActions = await getActionsForDevice(
    req.cookies["AUTH_SESSION_ID"] ?? req.cookies["AUTH_SESSION_ID_LEGACY"],
    "device");
  next();
}

const fetchCaptchaActions = async (req, res, next) => {
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  req._ipCaptchaActions = await getActionsForIP(ip, "captcha");
  req._deviceCaptchaActions = await getActionsForDevice(req.cookies["AUTH_SESSION_ID"] ?? req.cookies["AUTH_SESSION_ID_LEGACY"], "captcha");
  next();
}

/**
 * @name *\/openid-connect/auth*
 * @desc
 * Proxy everything Keycloak login form template fetch and inject fingerprintjs
 */
router.use("*/openid-connect/auth*", fetchCaptchaActions, createProxyMiddleware({
  target: process.env.KEYCLOAK_URL,
  logLevel: `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info",
  // pathFilter: "**/openid-connect/auth**",  // Micromatch
  pathFilter: "**",
  selfHandleResponse: true,
  ws: true,
  logger: logger,
  onProxyReq: (proxyReq, req, res) => {
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    proxyReq.setHeader("x-forwarded-for", ip);
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
      return responseBuffer;
  }),
}));

/**
 * @name *\/login-actions/authenticate*
 * @desc
 * Proxy everything Keycloak login post attempts to take actions
 */
router.use("*/login-actions/authenticate*", fetchCaptchaActions, fetchBlockActions, createProxyMiddleware({
  target: process.env.KEYCLOAK_URL,
  logLevel: `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info",
  pathFilter: "**",
  ws: true,
  logger: logger,
  onProxyReq: (proxyReq, req, res) => {

    if (req.path.includes("login-actions/authenticate") && req.method === "POST") {
  
      const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
      proxyReq.setHeader("x-forwarded-for", ip);
  
      if (req._ipBlockActions.rows.length > 0) {
          logger.debug("IP block");
          res.writeHead(429, {
            'Content-Type': 'text/plain',
          });
          res.end('Too many failed login attempts on this IP. Wait for cooldown.');
          return;
      }

      if (req._deviceBlockActions.rows.length > 0) {
        logger.debug("Device block");
        res.writeHead(429, {
          'Content-Type': 'text/plain',
        });
        res.end('Too many failed login attempts on this device. Wait for cooldown.');
        return
      }
  
      // const c = getDeviceByFingerprintCookie(req.cookies["DEVICE_FINGERPRINT"]);
    }
  },
  onProxyRes: (proxyRes, req, res) => {
    if (
      req.path.includes("login-actions/authenticate") &&
      req.method === "POST" && !res.finished) {
        if (res.statusCode === 302) {
          // TODO: notify user if new domain
        logger.debug("Login succeded, notify user if new device.")
        }
        if (req._ipCaptchaActions.rows.length > 0) {
          logger.debug("login-actions reCaptcha IP");
          res.setHeader('X-SUSPICIOUS-REQUEST', 1);
          return;
        };
    
        if (req._deviceCaptchaActions.rows.length > 0) {
          logger.debug("login-actions reCaptcha device");
          res.setHeader('X-SUSPICIOUS-REQUEST', 1);
          return;
        };
    };
  },
}));

/**
 * @name /
 * @desc
 * Proxy most of the requests not involving auth
 */
router.use("/", createProxyMiddleware({
  target: process.env.KEYCLOAK_URL,
  logLevel: `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info",
  pathFilter: "**",
  logger: logger
}));

module.exports = router;