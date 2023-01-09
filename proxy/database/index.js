const { getDeviceByIpOrUserAgent, getDeviceByCookie, getDeviceByFingerprintCookie } = require("./db");

module.exports = {
    getDeviceByIpOrUserAgent,
    getDeviceByCookie,
    getDeviceByFingerprintCookie
}