variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "data_region" {
  type        = string
  description = "Region for GCP Resources"
  default     = "us-central1"
}

variable "data_lakehouse_raw_bucket" {
  type        = string
  description = "GCS bucket for storing raw data"
}

variable "raw_stock_market_record_dataset" {
  type        = string
  description = "BigQuery Dataset for the raw data from stock record data"
}