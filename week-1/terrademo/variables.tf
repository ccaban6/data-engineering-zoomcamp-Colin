variable "creds" {
  description = "Credentials for Authentication"
  default     = "./keys/my-creds.json"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "turing-botany-446402-t2-terra-bucket"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "project" {
  description = "Project"
  default     = "turing-botany-446402-t2"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}