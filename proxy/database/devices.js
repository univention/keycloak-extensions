const { pool } = require("./db");


const saveFingerprintToDeviceRelation = async (device_fingerprint, keycloak_device_id, user_id) => {
  const date = new Date();
  result = await pool.query(
      'INSERT INTO devices (fingerprint_device_id, keycloak_device_id, user_id, is_notified, created_at) VALUES ($1, $2, $3, false, $4) ON CONFLICT DO NOTHING',
      [device_fingerprint, keycloak_device_id, user_id, date]);
  return result;
};
  
  
module.exports = {
  saveFingerprintToDeviceRelation,
}