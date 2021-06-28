resource "google_compute_network" "network" {
  name                    = var.env
  auto_create_subnetworks = "false"
}

resource "google_compute_subnetwork" "subnet-1" {
  name          = "${var.env}-subnet-1"
  ip_cidr_range = "192.168.${var.env == "dev" ? 10 : 20}.0/24"
  network       = google_compute_network.network.self_link
}
