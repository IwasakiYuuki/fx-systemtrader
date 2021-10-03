variable "cluster-name" {
  default = "data-analysis-cluster"
}

variable "cluster-location" {
  default = "us-central1-b"
}

variable "gke_default_sa-name" {
  default = "gke-default-sa"
}

variable "primary_node-name" {
  default = "preemptible-node-pool-1"
}

variable "primary_node-min_node_count" {
  default = 1
}

variable "primary_node-max_node_count" {
  default = 3
}

variable "primary_node-machine_type" {
  default = "e2-standard-2"
}

variable "primary_node-image_type" {
  default = "COS"
}
