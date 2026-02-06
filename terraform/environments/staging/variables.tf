variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "env" {
  type    = string
  default = "staging"
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "bq_dataset" {
  description = "The BigQuery dataset name"
  type        = string
}