const winston = require("winston");

const level = `${process.env.LOG_LEVEL}`.toLowerCase() ?? "info";

const logger = winston.createLogger({
  level,
  format: winston.format.json(),
  defaultMeta: { service: "proxy" },
  transports: [
    new winston.transports.Console({ level }),
    new winston.transports.File({ filename: "proxy.log", level}),
  ],
});

module.exports = {
  logger
};
