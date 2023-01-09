const { getDeviceByIpOrUserAgent, getDeviceByCookie, getDeviceByFingerprintCookie } = require("./devices");
const { getActionsForIP, getActionsForDevice } = require("./actions");

module.exports = {
    getDeviceByIpOrUserAgent,
    getDeviceByCookie,
    getDeviceByFingerprintCookie,
    getActionsForIP,
    getActionsForDevice
}