/*
 * Like what you see? Join us!
 * https://www.univention.com/about-us/careers/vacancies/
 *
 * Copyright 2020-2023 Univention GmbH
 *
 * https://www.univention.de/
 *
 * All rights reserved.
 *
 * The source code of this program is made available
 * under the terms of the GNU Affero General Public License version 3
 * (GNU AGPL V3) as published by the Free Software Foundation.
 *
 * Binary versions of this program provided by Univention to you as
 * well as other copyrighted, protected or trademarked materials like
 * Logos, graphics, fonts, specific documentations and configurations,
 * cryptographic keys etc. are subject to a license agreement between
 * you and Univention and not subject to the GNU AGPL V3.
 *
 * In the case you use this program under the terms of the GNU AGPL V3,
 * the program is provided in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License with the Debian GNU/Linux or Univention distribution in file
 * /usr/share/common-licenses/AGPL-3; if not, see
 * <https://www.gnu.org/licenses/>.
 */

const fs = require("node:fs");
const winston = require("winston");

const level = (process.env.LOG_LEVEL ?? "info").toLowerCase();

const logFile = process.env.LOG_FILE ?? "";

const logger = winston.createLogger({
  level,
  format: winston.format.json(),
  defaultMeta: { service: "proxy" },
  transports: [new winston.transports.Console({ level })],
});

// winston never reports a file it failed to open, it just retains every record
// in memory instead, so check up front rather than waiting for an error.
const canWrite = (filename) => {
  try {
    fs.closeSync(fs.openSync(filename, "a"));
    return true;
  } catch (error) {
    logger.error(
      `Not logging to ${filename}, it cannot be written: ${error.message}`,
    );
    return false;
  }
};

if (logFile && canWrite(logFile)) {
  const fileTransport = new winston.transports.File({
    filename: logFile,
    level,
    maxsize: 10 * 1024 * 1024,
    maxFiles: 3,
    tailable: true,
  });

  fileTransport.on("error", (error) => {
    logger.remove(fileTransport);
    logger.error(
      `Disabled the log file ${logFile}, it cannot be written: ${error.message}`,
    );
  });

  logger.add(fileTransport);
}

logger.on("error", (error) => {
  console.error(`Logger error: ${error.message}`);
});

module.exports = {
  logger
};
