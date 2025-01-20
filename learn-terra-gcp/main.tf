terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = "data-eng-20211212"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terrademo-bucket-2608"
  location      = "US"
  project       = "data-eng-20211212"
  storage_class = "STANDARD"

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
