variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "env" {
  description = "Environment (staging or prod)"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "asia-northeast1"
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

variable "bq_dataset" {
  description = "The BigQuery dataset name"
  type        = string
  # デフォルト値を staging にしておく
  default     = "celestial_biome_data_staging"
}

variable "domain_name" {
  description = "Custom domain name for the Cloud Run service"
  type        = string
  default     = "" # 指定しない場合はマッピングを作成しない
}