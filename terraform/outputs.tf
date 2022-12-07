output "server_ip" {
  value = hcloud_server.primary.ipv4_address
  description = "The IPv4 address of the created Hetzner server for this environment."
}

output "server_subdomain" {
  value = "${var.project_name_slug}-${var.target_environment}"
  description = "The subdomain for this environment."
}

output "server_https_url_primary" {
  value = length(aws_route53_record.primary) > 0 ? one(aws_route53_record.primary).name : null
  description = "The full domain name for the primary server for this environment."
}

output "server_https_url_portal" {
  value = length(aws_route53_record.portal) > 0 ? one(aws_route53_record.portal).name : null
  description = "The full domain name for the portal server for this environment."
}

output "server_https_url_ucs-sso" {
  value = length(aws_route53_record.ucs-sso) > 0 ? one(aws_route53_record.ucs-sso).name : null
  description = "The full domain name for the ucs-sso server for this environment."
}
