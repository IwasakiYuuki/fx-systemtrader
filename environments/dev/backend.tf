terraform {
  backend "gcs" {
    bucket = "fx-systemtrader-dev-tfstate"
    prefix = "env/dev"
  }
}
