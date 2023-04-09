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

const { pool } = require("./db");

const getActionCountForIP = async (ip, action) => {
  const result = await pool.query(
    "SELECT * FROM actions WHERE ip_address = $1 AND action = $2 ORDER BY expiration ASC",
    [ip, action]
  );
  return result.rowCount;
};

const getActionCountForDevice = async (code_id, action) => {
  const result = await pool.query(
    "SELECT * FROM actions WHERE keycloak_device_id = $1 AND action = $2 ORDER BY expiration ASC",
    [code_id, action]
  );
  return result.rowCount;
};

module.exports = {
  getActionCountForIP,
  getActionCountForDevice,
};
