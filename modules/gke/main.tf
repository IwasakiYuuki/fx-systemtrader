resource "google_service_account" "gke-default-sa" {
  account_id   = var.gke_default_sa-name
  display_name = "GKE service account"
  description  = "Default service account for GKE"
}

resource "google_container_cluster" "cluster-1" {
  provider = google-beta
  name     = var.cluster-name
  location = var.cluster-location

  // クラスターのデフォルトのノードをプリエンティブノードにするため削除
  remove_default_node_pool = true
  initial_node_count       = 1

  workload_identity_config {
    identity_namespace = "${var.project}.svc.id.goog"
  }

  cluster_autoscaling {
    enabled             = true
    autoscaling_profile = "OPTIMIZE_UTILIZATION"

    resource_limits {
      resource_type = "cpu"
      minimum       = 1
      maximum       = 8
    }

    resource_limits {
      resource_type = "memory"
      minimum       = 1
      maximum       = 32
    }
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

resource "google_container_node_pool" "gpu-node" {
  name = var.gpu_node-name

  cluster = google_container_cluster.cluster-1.id

  initial_node_count = 0

  autoscaling {
    min_node_count = var.gpu_node-min_node_count
    max_node_count = var.gpu_node-max_node_count
  }

  node_config {
    preemptible  = true
    machine_type = var.gpu_node-machine_type

    image_type = var.gpu_node-image_type

    guest_accelerator {
      type  = var.gpu_node-gpu_type
      count = var.gpu_node-gpu_count
    }

    service_account = google_service_account.gke-default-sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

resource "google_container_node_pool" "highmemory-node" {
  name = var.highmemory_node-name

  cluster = google_container_cluster.cluster-1.id

  initial_node_count = 0

  autoscaling {
    min_node_count = var.highmemory_node-min_node_count
    max_node_count = var.highmemory_node-max_node_count
  }

  node_config {
    machine_type = var.highmemory_node-machine_type

    // Argoがcos-containerdでは動かないため, cosに変更
    image_type = var.highmemory_node-image_type

    service_account = google_service_account.gke-default-sa.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    taint {
      key    = "highmem"
      value  = "present"
      effect = "NO_SCHEDULE"
    }
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
  argo_service_accounts = {
    argo-tutorial-sa = toset([
      "roles/editor",
    ]),
  }
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
//  source              = "terraform-google-modules/kubernetes-engine/google//modules/workload-identity"
//  use_existing_k8s_sa = true
//  for_each            = local.argo_service_accounts
//
//  name       = each.key
//  namespace  = "argo"
//  project_id = var.project
//  roles      = each.value
//}

module "test-workload-identity" {
  source        = "../workload_identity"
  project_id    = "fx-systemtrader-dev"
  account_id    = "argo-tutorial-sa"
  k8s_namespace = "argo"
  ksa_name      = "argo-tutorial-sa"
  roles         = ["roles/storage.admin"]
}
