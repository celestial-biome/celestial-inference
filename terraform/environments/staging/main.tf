module "inference_service" {
  source = "../../modules/inference_service"

  project_id = var.project_id
  env        = "staging"
  region     = "asia-northeast1"
  image_tag  = var.image_tag
  bq_dataset = "celestial_biome_data_staging"
  domain_name = "inference-staging.celestial-biome.com"
}

terraform {
  required_version = ">= 1.9.0"
  backend "gcs" {
    bucket = "celestial-biome-tfstate"
    prefix = "inference/staging"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = "asia-northeast1"
}


