terraform {
  backend "gcs" {
    bucket = "fx-systemtrader-tfstate"
    prefix = "env/dev"
  }
}
