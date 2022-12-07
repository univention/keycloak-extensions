variable "create_dns_record" {
  default = false
  type    = bool
  description = "Boolean value which indicates if a DNS record should be created."
}

variable "server_type_ucs" {
  default = "cx21"
  type    = string
  description = "The Hetzner VPS machine type for this server."
}

variable "server_ssh_keys" {
  default = [
    "4820687", # ucs
    "4872327", # arequate
  ]
  type = list(string)
  description = "A list of pre-installed SSH keys for this machine."
}

variable "server_snapshot" {
  #UCS 5.0
  default = "53389185"
  type    = string
  description = "The Hetzner source snapshot image to be used for this server."
}

variable "project_name_slug" {
  type    = string
  default = "default"
  description = "The slug for this project, used in domain names, labels, and tags."
}

variable "target_environment" {
  type        = string
  default     = "default"
  description = "The name for this environment. Used in domain names."

  validation {
    condition     = ( length(var.target_environment) < 255 )
    error_message = "The length of var.target_environment cannot exceed 255 characters."
  }

  validation {
    condition     = ( length(var.target_environment) > 0 )
    error_message = "The variable var.target_environment must not be empty."
  }
}
