provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
  region  = var.region
}

module "vpc" {
  source = "../../modules/vpc"
  env    = var.env
}

module "firewall" {
  source  = "../../modules/firewall"
  network = module.vpc.network
}

module "dummy-api" {
  source = "../../modules/dummy-api"
  zone   = var.zone
  subnet = module.vpc.subnet-1
}

module "get-rates" {
  source  = "../../modules/get_rates"
  project = var.project
  vpc-con = module.vpc.subnet-1-vpc-con
}
