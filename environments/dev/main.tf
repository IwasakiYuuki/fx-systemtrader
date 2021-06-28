locals {
  env = "dev"
}

provider "google" {
  project = var.project
  region  = var.region
}

module "vpc" {
  source = "../../modules/vpc"
  env    = local.env
}

module "dummy-api" {
  source = "../../modules/dummy-api"
  zone   = var.zone
  subnet = module.vpc.subnet-1
}
#
#resource "google_compute_network" "default" {
#  name                    = "fx-systemtrader-vpc"
#  auto_create_subnetworks = "false"
#}
#
#resource "google_compute_subnetwork" "subnet-1" {
#  name          = "subnet-1"
#  ip_cidr_range = "192.168.1.0/24"
#  network       = google_compute_network.default.self_link
#}
#
#module "dummy-api-container" {
#  source = "github.com/terraform-google-modules/terraform-google-container-vm"
#
#  container = {
#    image = "gcr.io/fx-systemtrader/dummy-api"
#  }
#
#  restart_policy = "Always"
#}
#
#resource "google_compute_instance" "dummy-api" {
#  name         = "dummy-api"
#  machine_type = "f1-micro"
#  zone         = var.zone
#
#  boot_disk {
#    auto_delete = true
#    initialize_params {
#      image = module.dummy-api-container.source_image
#    }
#  }
#
#  network_interface {
#    subnetwork = google_compute_subnetwork.subnet-1.name
#  }
#
#  metadata = {
#    gce-container-declaration = module.dummy-api-container.metadata_value
#  }
#
#  service_account {
#    scopes = [
#      "https://www.googleapis.com/auth/cloud-platform"
#    ]
#  }
#}
