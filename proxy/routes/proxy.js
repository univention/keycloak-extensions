const express = require("express");
const jwt_decode = require("jwt-decode");
const setCookie = require('set-cookie-parser');
const { createProxyMiddleware, responseInterceptor } = require("http-proxy-middleware");

const {
    logger,
    injectFingerprintJS,
    injectGoogleCaptcha
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

// Re-use the same proxy middleware when proxying both SAML and OIDC urls.
// Proxy the login form and inject FingerprintJs.
const loginMiddleware = createProxyMiddleware({
  target: process.env.KEYCLOAK_URL,
  logLevel: `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info",
  pathFilter: "**",
  ws: true,
  selfHandleResponse: true,
  logger: logger,

  onProxyReq: (proxyReq, req, res) => {
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    proxyReq.setHeader("x-forwarded-for", ip);
  },

  onProxyRes: responseInterceptor(async (responseBuffer, proxyRes, req, res) => {
    if (res.writableEnded)
      return responseBuffer;

    if (
      (req.path.includes("openid-connect/auth") || req.path.includes("protocol/saml"))
      && req.method === "GET"
      && (proxyRes.headers['content-type'] ?? "").includes("text/html")
    ) {
      logger.debug(`Injecting script into ${req.method} ${req.path}`);
      const response = responseBuffer.toString('utf8'); // Convert buffer to string
      return injectFingerprintJS(response);
    };
    return responseBuffer;
  }),
});

/**
 * @name *\/protocol/saml*
 * @desc
 * Proxy the Keycloak SAML login form and inject fingerprintjs.
 */
router.use("*/protocol/saml*", fetchCaptchaActions, loginMiddleware);

/**
 * @name *\/openid-connect/auth*
 * @desc
 * Proxy the Keycloak OIDC login form and inject fingerprintjs.
 */
router.use("*/openid-connect/auth*", fetchCaptchaActions, loginMiddleware);

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
        req.path.includes("login-actions/authenticate") && req.method === "POST"
        && (200 <= res.statusCode) && (res.statusCode <= 399)
    ) {
      const resCookies = setCookie.parse(proxyRes, {map: true});
      const rawToken = (resCookies["KEYCLOAK_IDENTITY"] || resCookies["KEYCLOAK_IDENTITY_LEGACY"])?.value;
      if (rawToken === undefined) {
        logger.warn("POST to login-actions/authenticate without Keycloak identity tokens!");
        return responseBuffer;
      }
      const token = jwt_decode(rawToken);

      if (Object.keys(req.cookies).includes("DEVICE_FINGERPRINT")) {
        logger.debug("Login succeeded, notify user if new device.");
        await saveFingerprintToDeviceRelation(
          req.cookies["DEVICE_FINGERPRINT"],
          req.cookies["AUTH_SESSION_ID"] ?? req.cookies["AUTH_SESSION_ID_LEGACY"],
          token.sub,
        );
      } else {
        logger.info("Login succeeded, but no fingerprint was returned.");
      }

      if (res.statusCode === 200 && (req._ipCaptchaActions.rows.length > 0 || req._deviceCaptchaActions.rows.length > 0)) {
        logger.debug("Prompting for reCaptcha");
        let response = responseBuffer.toString('utf8');
        return injectGoogleCaptcha(response);
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