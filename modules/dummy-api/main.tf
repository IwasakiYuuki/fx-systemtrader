module "dummy-api-container" {
  source = "github.com/terraform-google-modules/terraform-google-container-vm"

  container = {
    image = "gcr.io/fx-systemtrader/dummy-api"
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "dummy-api" {
  zone         = var.zone
  name         = "dummy-api"
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      image = module.dummy-api-container.source_image
    }
  }

  network_interface {
    subnetwork = var.subnet
  }

  metadata = {
    gce-container-declaration = module.dummy-api-container.metadata_value
  }

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
