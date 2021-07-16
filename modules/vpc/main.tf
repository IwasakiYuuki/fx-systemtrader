/**
 * 開発環境用のVPC。
 * 基本的にはこの中にほとんどのリソースを格納する。
 * 現段階ではリージョンをus-central1設定している。（VMインスタンスがそのリージョン内で無料なため）
 */
resource "google_compute_network" "network" {
  name                    = var.env
  auto_create_subnetworks = "false"
}

/**
 * 開発環境用のサブネットワーク１。 
 * このサブネットはFX APIからデータを取得・保存するためのインスタンスなどを配置するために作成した。 
 * 環境ごとにGCPプロジェクトごと分けるため、CIDRは変更しない。
 */
resource "google_compute_subnetwork" "subnet-1" {
  name          = "subnet-1"
  ip_cidr_range = "192.168.10.0/24"
  network       = google_compute_network.network.self_link
}

/**
 * 開発環境サーバレスVPCアクセス用のサブネットワーク２。
 * このサブネットはサブネットワーク１とCloud FuntionsなどのVPC外のリソースを内部通信させるためのもの。
 * Cloud Funtionsなどはデフォルトでは外部を通して通信するためファイアウォールを設定しなければならない。
 */
resource "google_compute_subnetwork" "subnet-2" {
  name          = "subnet-2"
  ip_cidr_range = "192.168.8.0/28"
  network       = google_compute_network.network.self_link
}

/**
 * Cloud NAT用のルータ。
 */
resource "google_compute_router" "router-1" {
  name    = "router-1"
  region  = google_compute_subnetwork.subnet-1.region
  network = google_compute_network.network.id
}

/**
 * 外部IPを持たないインスタンスがインターネット接続するためのCloud NAT。
 */
resource "google_compute_router_nat" "nat-1" {
  name                               = "nat-1"
  router                             = google_compute_router.router-1.name
  region                             = google_compute_router.router-1.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"

  subnetwork {
    name                    = google_compute_subnetwork.subnet-1.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
}

/**
 * サーバーレスVPCアクセス用のコネクター。
 * Cloud FuntionsなどのVPC外のリソースを内部通信させるためのもの。
 */
resource "google_vpc_access_connector" "subnet-1-vpc-con" {
  provider = google-beta
  name     = "subnet-1-vpc-con"
  subnet {
    name = google_compute_subnetwork.subnet-2.name
  }
  machine_type = "f1-micro"
}
