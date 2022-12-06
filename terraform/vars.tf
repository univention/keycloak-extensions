variable "server_type_ucs" {
  default = "cx21"
  type    = string
}

variable "create_dns_record" {
  default = false
  type    = bool
}

variable "project_name" {
  type    = string
  default = "default"
}

variable "server_ssh_keys" {
  default = [
    "4820687", # ucs
    "4872327", # arequate
  ]
  type = list(string)
}

variable "server_snapshot" {
  #UCS 5.0
  default = "53389185"
  type    = string
}

variable "ci_target_environment" {
  type        = string
  default     = "default"
  description = "The name for this environment. Used in domain names as well."

  validation {
    condition     = ( length(var.ci_target_environment) < 255 )
    error_message = "The length of var.ci_target_environment cannot exceed 255 characters."
  }

  validation {
    condition     = ( length(var.ci_target_environment) > 0 )
    error_message = "The variable var.ci_target_environment must not be empty."
  }
}
