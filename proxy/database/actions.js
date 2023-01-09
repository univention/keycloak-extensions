const { pool } = require("./db");

  
const getActionsForIP = async (ip, action) => {
  const result = await pool.query('SELECT * FROM actions WHERE ip_address = $1 AND action = $2 ORDER BY expiration ASC', [ip, action]);
  return result;
};

const getActionsForDevice = async (code_id, action) => {
  const result = await pool.query('SELECT * FROM actions WHERE keycloak_device_id = $1 AND action = $2 ORDER BY expiration ASC', [code_id, action]);
  return result;
};

  
  module.exports = {
    getActionsForIP,
    getActionsForDevice,
  }