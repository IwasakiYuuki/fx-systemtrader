output "network" {
  value = google_compute_network.network.name
}

output "subnet-1" {
  value = google_compute_subnetwork.subnet-1.name
}
