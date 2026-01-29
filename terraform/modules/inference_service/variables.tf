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
