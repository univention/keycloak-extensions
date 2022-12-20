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

# TODO: Clean this up, for obvious security reasons.
variable "server-ssh-keys" {
  default = [
    "4820687", # ucs
    "4872327", # arequate
  ]
  type = list(string)
}

# TODO: Find out where a list of these images can be found.
variable "server-snapshot" {
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
