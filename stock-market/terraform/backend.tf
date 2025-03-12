terraform {
  backend "gcs" {
    bucket = "01shuokai-gcp-labs-tfstate01"
    prefix = "terraform/state"
  }
}