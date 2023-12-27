# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

output "server_ip" {
  value = hcloud_server.main.ipv4_address
}
