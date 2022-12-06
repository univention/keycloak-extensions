# For the AWS resources used in this configuration, please see the docs at:
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_zone

terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "1.32.2"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "3.7.0"
    }
  }
  backend "http" {
  }
}

provider "aws" {
  region  = "eu-west-1"
  profile = "univention"
}

provider "hcloud" {
}

resource "hcloud_server" "main" {
  name        = "${var.project_name}-primary-${var.project_name}-${var.ci_target_environment}"
  server_type = var.server_type_ucs
  image       = var.server_snapshot
  location    = "fsn1"
  ssh_keys    = var.server_ssh_keys
  keep_disk   = true

  labels = {
    dns_record   = "${var.project_name}-${var.ci_target_environment}"
    project_name = var.project_name
    purpose      = "primary"
  }

  backups = false
}

data "aws_route53_zone" "at-univention_de" {
  zone_id      = "Z02289031NQM37687COIB"
  private_zone = false
}

resource "aws_route53_record" "primary" {
  count = var.create_dns_record ? 1 : 0
  name  = "primary.${var.project_name}-${var.ci_target_environment}.${data.aws_route53_zone.at-univention_de.name}"
  type  = "A"

  records = [
    hcloud_server.main.ipv4_address
  ]

  ttl     = 300
  zone_id = data.aws_route53_zone.at-univention_de.zone_id

  depends_on = [
    hcloud_server.main
  ]
}

resource "aws_route53_record" "portal" {
  count = var.create_dns_record ? 1 : 0
  name  = "portal.${var.project_name}-${var.ci_target_environment}.${data.aws_route53_zone.at-univention_de.name}"
  type  = "A"

  records = [
    hcloud_server.main.ipv4_address
  ]

  ttl     = 300
  zone_id = data.aws_route53_zone.at-univention_de.zone_id

  depends_on = [
    hcloud_server.main
  ]
}

resource "aws_route53_record" "ucs-sso" {
  count = var.create_dns_record ? 1 : 0
  name  = "ucs-sso.${var.project_name}-${var.ci_target_environment}.${data.aws_route53_zone.at-univention_de.name}"
  type  = "A"

  records = [
    hcloud_server.main.ipv4_address
  ]

  ttl     = 300
  zone_id = data.aws_route53_zone.at-univention_de.zone_id

  depends_on = [
    hcloud_server.main
  ]
}

