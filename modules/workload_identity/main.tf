resource "google_service_account" "sa" {
  account_id   = var.account_id
  display_name = var.display_name
  description  = var.description
}

resource "google_service_account_iam_member" "workload_identity_member" {
  service_account_id = google_service_account.sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.k8s_namespace}/${var.ksa_name}]"
}

resource "google_project_iam_member" "member" {
  count  = length(var.roles)
  role   = element(var.roles, count.index)
  member = "serviceAccount:${google_service_account.sa.email}"
}
