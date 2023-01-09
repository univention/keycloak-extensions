const Pool = require('pg').Pool
const pool = new Pool({
  user: process.env.DB_USER ?? "postgres",
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
})

const getDeviceByIpOrUserAgent = async (ip, userAgent) => {
  // TODO: user_agent doesn't exist yet on the database (modify handler)... should it?
  const result = await pool.query('SELECT * FROM actions WHERE ip_address = $1 OR user_agent = $2', [ip, userAgent]);
  return result;
};

const getDeviceByCookie = async (cookie_uuid) => {
  const result = await pool.query('SELECT * FROM actions WHERE uuid = $1', [cookie_uuid]);
  return result;
};

const getDeviceByFingerprintCookie = async (fingerprint_uuid) => {
  const result = await pool.query('SELECT * FROM actions WHERE uuid = $1', [fingerprint_uuid]);
  return result;
};

module.exports = {
  getDeviceByIpOrUserAgent,
  getDeviceByCookie,
  getDeviceByFingerprintCookie,
}