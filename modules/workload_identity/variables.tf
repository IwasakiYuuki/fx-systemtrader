variable "project_id" {}

variable "account_id" {}

variable "display_name" {
  default = "Workload Identity Service Account"
}

variable "description" {
  default = "Workload Identity Service Account"
}

variable "k8s_namespace" {}

variable "ksa_name" {}

variable "roles" {
  default = []
}
