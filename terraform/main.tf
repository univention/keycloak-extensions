# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
      version = "1.45.0"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.42.0"
    }
  }
  backend "http" {
  }
}

provider "aws" {
  region                  = "eu-west-1"
  profile                 = "univention"
}

provider "hcloud" {
}

resource "hcloud_server" "main" {
  name        = "${var.project-name}-primary-${var.dns-domain}"
  server_type = var.server-type-ucs
  image       = var.server-snapshot
  location    = "fsn1"
  ssh_keys    = var.server-ssh-keys
  keep_disk   = true

  labels           = {
    dns_record     = var.dns-domain
    project_id     = var.project-id
    project_name   = var.project-name
    purpose        = "primary"
  }

  backups = false
}

data "aws_route53_zone" "at-univention_de" {
  zone_id      = "Z02289031NQM37687COIB"
  private_zone = false
}

resource "aws_route53_record" "master" {
  # Control if a DNS record should be created.
  count = var.create-dns-record ? 1 : 0

  # The name of the record [string].
  name = "master.${var.dns-domain}.${data.aws_route53_zone.at-univention_de.name}"

  # The record type [string].
  # Possible values: "A", "AAAA", "NS", "TXT", ...
  type = "A"

  # The record content, as a set of strings [list].
  records = [
    hcloud_server.main.ipv4_address
  ]

  # The TTL to set for the records [integer].
  ttl = 300

  # The ID of the hosted zone to contain this record [string].
  zone_id = data.aws_route53_zone.at-univention_de.zone_id

  depends_on = [
    hcloud_server.main
  ]
}

resource "aws_route53_record" "portal" {
  # Control if a DNS record should be created.
  count = var.create-dns-record ? 1 : 0

  # The name of the record [string].
  name = "portal.${var.dns-domain}.${data.aws_route53_zone.at-univention_de.name}"

  # The record type [string].
  # Possible values: "A", "AAAA", "NS", "TXT", ...
  type = "A"

  # The record content, as a set of strings [list].
  records = [
    hcloud_server.main.ipv4_address
  ]

  # The TTL to set for the records [integer].
  ttl = 300

  # The ID of the hosted zone to contain this record [string].
  zone_id = data.aws_route53_zone.at-univention_de.zone_id

  depends_on = [
    hcloud_server.main
  ]
}

resource "aws_route53_record" "ucs-sso" {
  # Control if a DNS record should be created.
  count = var.create-dns-record ? 1 : 0

  # The name of the record [string].
  name = "ucs-sso.${var.dns-domain}.${data.aws_route53_zone.at-univention_de.name}"

  type = "A"

  # The record content, as a set of strings [list].
  records = [
    hcloud_server.main.ipv4_address
  ]

  # The TTL to set for the records [integer].
  ttl = 300

  # The ID of the hosted zone to contain this record [string].
  zone_id = data.aws_route53_zone.at-univention_de.zone_id

  depends_on = [
    hcloud_server.main
  ]
}
