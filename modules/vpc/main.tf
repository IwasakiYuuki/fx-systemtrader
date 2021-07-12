resource "google_compute_network" "network" {
  name                    = var.env
  auto_create_subnetworks = "false"
}

resource "google_compute_subnetwork" "subnet-1" {
  name          = "subnet-1"
  ip_cidr_range = "192.168.10.0/24"
  network       = google_compute_network.network.self_link
}

resource "google_compute_subnetwork" "subnet-2" {
  name          = "${var.env}-subnet-2"
  ip_cidr_range = "192.168.8.0/28"
  network       = google_compute_network.network.self_link
}

resource "google_vpc_access_connector" "subnet-1-vpc-con" {
  provider = google-beta
  name     = "subnet-1-vpc-con"
  subnet {
    name = google_compute_subnetwork.subnet-2.name
  }
  machine_type = "f1-micro"
}

resource "google_compute_firewall" "local-http" {
  name    = "local-http-firewall"
  network = google_compute_network.network.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["192.168.0.0/16"]
}
