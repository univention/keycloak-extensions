const express = require("express");
const jwt_decode = require("jwt-decode");
const setCookie = require('set-cookie-parser');
const { createProxyMiddleware, responseInterceptor } = require("http-proxy-middleware");

const {
    logger
} = require("../utils");

const { 
  saveFingerprintToDeviceRelation,
  getActionsForIP,
  getActionsForDevice,
} = require("../database");
const { response } = require("express");

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

const applyBlocks = (req, res, next) => {

  if (req.method !== "POST") next();
  if (req._deviceBlockActions.rows.length === 0 && req._ipBlockActions.rows.length === 0) next();
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
    return;
  }
};

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
      if (res.writableEnded) return responseBuffer;
      if (
      req.path.includes("openid-connect/auth") &&
      req.method === "GET" &&
      (proxyRes.headers['content-type'] ?? "").includes("text/html")
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
router.use("*/login-actions/authenticate*", fetchCaptchaActions, fetchBlockActions, applyBlocks, createProxyMiddleware({
  target: process.env.KEYCLOAK_URL,
  logLevel: `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info",
  pathFilter: "**",
  ws: true,
  selfHandleResponse: true,
  logger: logger,
  onProxyReq: (proxyReq, req, res) => {

    if (req.path.includes("login-actions/authenticate") && req.method === "POST") {
  
      const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
      proxyReq.setHeader("x-forwarded-for", ip);
    }
  },
  onProxyRes: responseInterceptor(async (responseBuffer, proxyRes, req, res) => {
    if (
      req.path.includes("login-actions/authenticate") &&
      req.method === "POST" ) {
        if (res.statusCode === 302) {
          logger.debug("Login succeded, notify user if new device.")
          // logger.debug(req.headers["set-cookie"])
          const cookies = setCookie.parse(proxyRes, {map: true});
          logger.debug(cookies);
          const token = jwt_decode(cookies["KEYCLOAK_IDENTITY"].value ?? cookies["KEYCLOAK_IDENTITY_LEGACY"].value)
          logger.debug(token)
          await saveFingerprintToDeviceRelation(
            req.cookies["DEVICE_FINGERPRINT"],
            req.cookies["AUTH_SESSION_ID"] ?? req.cookies["AUTH_SESSION_ID_LEGACY"],
            token.sub
          );
      }
    };
    return responseBuffer;
  }),
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