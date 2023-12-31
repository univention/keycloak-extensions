# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

variable "server-type-ucs" {
  default = "cx21"
  type    = string
}

variable "create-dns-record" {
  default = false
  type    = bool
}

variable "dns-domain" {
  default = "unassigned"
  type    = string
}

variable "project-id" {
  default = "0"
  type    = string
}

variable "project-name" {
  default = "keycloak"
  type    = string
}

variable "server-ssh-keys" {
  default = [
    "4820687", # ucs
    "4872327", # arequate
    "5715204"  # yschmidt
  ]
  type    = list(string)
}

variable "server-snapshot" {
  #UCS 5.0
  default = "53389185"
  type    = string
}

variable "ci_commit_ref_name" {
  default = "missing-ci-commit-ref-name"
  type = string
}
