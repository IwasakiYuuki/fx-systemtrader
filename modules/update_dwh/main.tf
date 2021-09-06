resource "google_service_account" "invocation-user" {
  project      = var.project
  account_id   = "invocation-user-2"
  display_name = "Invocation Service Account for update_dwh"
}

resource "google_project_iam_member" "add-role-1" {
  project = var.project
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.invocation-user.email}"
}

resource "google_project_iam_member" "add-role-2" {
  project = var.project
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.invocation-user.email}"
}

data "archive_file" "update_dwh" {
  type        = "zip"
  source_dir  = "../../fst/update_dwh"
  output_path = "${path.module}/source.zip"
}

resource "google_storage_bucket_object" "archive" {
  name   = "update_dwh-${data.archive_file.update_dwh.output_md5}.zip"
  bucket = "update_dwh-bucket"
  source = data.archive_file.update_dwh.output_path
}

resource "google_cloudfunctions_function" "function" {
  name        = "update_dwh"
  description = "Get rates data from OANDA API"
  runtime     = "python39"

  available_memory_mb           = 1024
  source_archive_bucket         = "update_dwh-bucket"
  source_archive_object         = google_storage_bucket_object.archive.name
  trigger_http                  = true
  timeout                       = 300
  entry_point                   = "update_dwh"
  vpc_connector                 = var.vpc-con
  vpc_connector_egress_settings = "PRIVATE_RANGES_ONLY"
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.invocation-user.email}"
}

resource "google_cloud_scheduler_job" "job" {
  name             = "update_dwh_job"
  schedule         = "15 0 * * 2-6"
  time_zone        = "Etc/UTC"
  attempt_deadline = "300s"

  http_target {
    http_method = "GET"
    uri         = google_cloudfunctions_function.function.https_trigger_url

    oidc_token {
      service_account_email = google_service_account.invocation-user.email
    }
  }
}
