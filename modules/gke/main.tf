resource "google_service_account" "gke-default-sa" {
  account_id   = var.gke_default_sa-name
  display_name = "GKE service account"
  description  = "Default service account for GKE"
}

resource "google_container_cluster" "cluster-1" {
  name     = var.cluster-name
  location = var.cluster-location

  // クラスターのデフォルトのノードをプリエンティブノードにするため削除
  remove_default_node_pool = true
  initial_node_count       = 1

  workload_identity_config {
    identity_namespace = "${var.project}.svc.id.goog"
  }
}

// プリエンティブノード
// vCPU:2, Memory:8GB
// イメージ：Dockerを使用するContainer-Optimized OS（cos）
// ブートディスク：100GB
// 目的：Argoサーバ，MLFlowサーバなどの常駐プログラム用．
resource "google_container_node_pool" "node-1" {
  name = var.primary_node-name

  cluster = google_container_cluster.cluster-1.id

  initial_node_count = 1

  autoscaling {
    min_node_count = var.primary_node-min_node_count
    max_node_count = var.primary_node-max_node_count
  }

  node_config {
    preemptible  = true
    machine_type = var.primary_node-machine_type

    // Argoがcos-containerdでは動かないため, cosに変更
    image_type = var.primary_node-image_type

    service_account = google_service_account.gke-default-sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

// Kubernetesに必要なサービスアカウントをmapにして，
// 下のモジュールで一括作成している
locals {
  default_service_accounts = {
    mlflow-sa = toset([
      "roles/storage.admin",
    ]),
  }
  //  argo_service_accounts = {
  //    argo-sa = toset([
  //      "roles/editor",
  //    ]),
  //  }
}

// このモジュールでは
//  １．Googleサービスアカウントの作成
//  ２．GoogleサービスアカウントへWorkload Identityのロールバインド
//  ３．Googleサービスアカウントへ指定された権限の付与
//  ４．対応するKubernetesサービスアカウントの作成
//  ５．Kubernetesサービスアカウントへのアノテーション
// を行っている．
module "default-workload-identity" {
  source   = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
  for_each = local.default_service_accounts

  name       = each.key
  namespace  = "default"
  project_id = var.project
  roles      = each.value
}

//module "argo-workload-identity" {
//  source   = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
//  for_each = local.argo_service_accounts
//
//  name       = each.key
//  namespace  = "argo"
//  project_id = var.project
//  roles      = each.value
//}
