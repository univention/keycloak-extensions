const Pool = require('pg').Pool
const pool = new Pool({
  user: process.env.POSTGRES_USER ?? "postgres",
  host: process.env.POSTGRES_HOST,
  database: process.env.POSTGRES_DATABASE_NAME,
  password: process.env.POSTGRES_PASSWORD,
  port: process.env.POSTGRES_PORT,
})

module.exports = {
  pool
}