const { logger } = require("./logger");
const { injectFingerprintJS, injectGoogleCaptcha } = require("./injectors");

module.exports = {
  logger,
  injectFingerprintJS,
  injectGoogleCaptcha
};
