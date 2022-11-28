output "server_ip" {
  value = hcloud_server.main.ipv4_address
}

output "server_https_url_primary" {
  value = aws_route53_record.primary.name
}

output "server_https_url_portal" {
  value = aws_route53_record.portal.name
}

output "server_https_url_ucs-sso" {
  value = aws_route53_record.ucs-sso.name
}
