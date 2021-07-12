module "dummy-api-container" {
  source = "github.com/terraform-google-modules/terraform-google-container-vm"

  container = {
    name  = "dummy-api"
    image = "gcr.io/fx-systemtrader-dev/dummy-api"
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "dummy-api-1" {
  zone         = var.zone
  name         = "dummy-api-1"
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      type  = "pd-standard"
      image = module.dummy-api-container.source_image
    }
  }

  network_interface {
    subnetwork = var.subnet
    network_ip = "192.168.10.10"
    access_config {}
  }

  metadata = {
    gce-container-declaration = module.dummy-api-container.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }

  labels = {
    container-vm = module.dummy-api-container.vm_container_label
  }

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
