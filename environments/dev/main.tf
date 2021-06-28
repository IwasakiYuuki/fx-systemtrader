provider "google" {
  project = var.project
  region  = var.region
}

module "vpc" {
  source = "../../modules/vpc"
  env    = var.env
}

module "dummy-api" {
  source = "../../modules/dummy-api"
  zone   = var.zone
  subnet = module.vpc.subnet-1
}
