resource "google_compute_firewall" "local-http" {
  name    = "local-http-firewall"
  network = var.network

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["192.168.0.0/16"]
}
