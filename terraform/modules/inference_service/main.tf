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
      image = "asia-northeast1-docker.pkg.dev/${var.project_id}/celestial-inference/inference:latest"
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
    }
  }
}

resource "google_artifact_registry_repository" "inference_repo" {
  location      = var.region
  repository_id = "celestial-inference" # ここを Actions の IMAGE_NAME と合わせる
  format        = "DOCKER"
}

# Vertex AI API の有効化
resource "google_project_service" "aiplatform" {
  project = var.project_id
  service = "aiplatform.googleapis.com"

  # 誤って無効化して他のサービスを止めないための安全策
  disable_on_destroy = false
}