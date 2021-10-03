provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
  region  = var.region
}

//===============
// Network module
//===============
module "vpc" {
  source = "../../modules/vpc"
  env    = var.env
}

//================
// Firewall module
//================
module "firewall" {
  source  = "../../modules/firewall"
  network = module.vpc.network
}

////=====================
//// A dummy of OANDA API
////=====================
//module "dummy-api" {
//  source = "../../modules/dummy-api"
//  zone   = var.zone
//  subnet = module.vpc.subnet-1
//}

////================
//// GKE module
////================
//module "gke" {
//  source = "../../modules/gke"
//}

//================================
// The function to get daily rates
//================================
module "get-rates" {
  source  = "../../modules/get_rates"
  project = var.project
  vpc-con = module.vpc.subnet-1-vpc-con
}

//================================
// The function to get daily rates
//================================
module "update-dwh" {
  source  = "../../modules/update_dwh"
  project = var.project
  vpc-con = module.vpc.subnet-1-vpc-con
}
