variable "project" {
}

variable "k8s_namespace" {
  default = "default"
}

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

variable "gpu_node-name" {
  default = "gpu-node-1"
}

variable "gpu_node-min_node_count" {
  default = 0
}

variable "gpu_node-max_node_count" {
  default = 1
}

variable "gpu_node-image_type" {
  default = "COS"
}

variable "gpu_node-machine_type" {
  default = "n1-standard-2"
}

variable "gpu_node-gpu_type" {
  default = "nvidia-tesla-t4"
}

variable "gpu_node-gpu_count" {
  default = 1
}

variable "highmemory_node-name" {
  default = "highmemory-node-pool-1"
}

variable "highmemory_node-min_node_count" {
  default = 0
}

variable "highmemory_node-max_node_count" {
  default = 3
}

variable "highmemory_node-machine_type" {
  default = "n2-highmem-2"
}

variable "highmemory_node-image_type" {
  default = "COS"
}
