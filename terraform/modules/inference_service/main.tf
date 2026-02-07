# Cloud Run 用の専用サービスアカウントを作成 
resource "google_service_account" "inference_sa" {
  account_id   = "inference-service-sa-${var.env}"
  display_name = "Inference Service Account for ${var.env}"
}

# 作成した SA に Vertex AI の利用権限を付与
resource "google_project_iam_member" "ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.inference_sa.email}"
}

# Cloud Run の定義でこの SA を使用するように指定
resource "google_cloud_run_v2_service" "inference" {
  name     = "inference-service-${var.env}"
  location = var.region

  template {
    containers {
      image = "asia-northeast1-docker.pkg.dev/${var.project_id}/celestial-inference-${var.env}/inference:${var.image_tag}"
      ports {
        container_port = 8080 # ここをDockerfileの起動ポートと合わせる
      }
      
      resources {
        limits = {
          cpu    = "2"      # LLM推論用に2CPU
          memory = "2Gi"    # メモリを2GiBに増強
        }
      }

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }

      env {
        name  = "BQ_DATASET"
        value = var.bq_dataset
      }
    }

    labels = {
      "commit-sha" = substr(var.image_tag, 0, 63)
    }
  }
}

resource "google_artifact_registry_repository" "inference_repo" {
  location      = var.region
  repository_id = "celestial-inference-${var.env}" # ここを Actions の IMAGE_NAME と合わせる
  format        = "DOCKER"
}

# Vertex AI API の有効化
resource "google_project_service" "aiplatform" {
  project = var.project_id
  service = "aiplatform.googleapis.com"

  # 誤って無効化して他のサービスを止めないための安全策
  disable_on_destroy = false
}

# 未認証のアクセスを許可する設定（staging の確認に限り）
resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.inference.location
  name     = google_cloud_run_v2_service.inference.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# BigQuery のジョブ実行権限
resource "google_project_iam_member" "bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.inference_sa.email}"
}

# データの閲覧権限
resource "google_project_iam_member" "bq_data_viewer" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.inference_sa.email}"
}

# ドメインマッピングの設定
resource "google_cloud_run_domain_mapping" "domain_map" {
  # domain_name が空でない場合のみ作成
  count    = var.domain_name != "" ? 1 : 0
  location = var.region
  name     = var.domain_name

  metadata {
    namespace = var.project_id
  }

  spec {
    # マッピング先のサービス名
    route_name = google_cloud_run_v2_service.inference.name
  }
}