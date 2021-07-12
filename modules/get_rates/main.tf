resource "google_service_account" "invocation-user" {
  project      = var.project
  account_id   = "invocation-user"
  display_name = "Invocation Service Account"
}

resource "google_project_iam_member" "add-role-1" {
  project = var.project
  role    = "roles/storage.objectCreator"
  member  = "serviceAccount:${google_service_account.invocation-user.email}"
}

data "archive_file" "get_rates" {
  type        = "zip"
  source_dir  = "../../fst/get_rates"
  output_path = "${path.module}/source.zip"
}

resource "google_storage_bucket" "bucket" {
  name = "get-rates-bucket"
}

resource "google_storage_bucket_object" "archive" {
  name   = "get_rates-${data.archive_file.get_rates.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.get_rates.output_path
}

resource "google_storage_bucket" "datalake" {
  name = "${var.project}-datalake"
}

resource "google_cloudfunctions_function" "function" {
  name        = "get_rates"
  description = "Get rates data from OANDA API"
  runtime     = "python39"

  available_memory_mb           = 128
  source_archive_bucket         = google_storage_bucket.bucket.name
  source_archive_object         = google_storage_bucket_object.archive.name
  trigger_http                  = true
  timeout                       = 60
  entry_point                   = "get_rates"
  vpc_connector                 = var.vpc-con
  vpc_connector_egress_settings = "PRIVATE_RANGES_ONLY"
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.invocation-user.email}"
}
