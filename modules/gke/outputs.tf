output "endpoint" {
  value = google_container_cluster.cluster-1.endpoint
}

output "ca_certificate" {
  value = google_container_cluster.cluster-1.master_auth[0].cluster_ca_certificate
}
