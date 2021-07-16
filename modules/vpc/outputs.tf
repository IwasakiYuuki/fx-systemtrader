output "network" {
  value = google_compute_network.network.name
}

output "subnet-1" {
  value = google_compute_subnetwork.subnet-1.name
}

output "subnet-2" {
  value = google_compute_subnetwork.subnet-2.name
}

output "router-1" {
  value = google_compute_router.router-1.name
}

output "subnet-1-vpc-con" {
  value = google_vpc_access_connector.subnet-1-vpc-con.self_link
}
