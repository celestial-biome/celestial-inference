variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "env" {
  type    = string
  default = "prod"
}

variable "image_tag" {
  type    = string
  default = "latest"
}
