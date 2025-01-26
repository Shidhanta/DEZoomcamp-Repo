variable "AWS_ACCESS_KEY_ID" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "AWS_REGION" {
  description = "AWS region"
  type        = string
  sensitive   = true
}

variable "S3_BUCKET_NAME" {
  description = "S3 bucket name"
  type        = string
}

variable "S3_BUCKET_TAGS" {
  description = "Tags to be applied to the S3 bucket"
  type        = map(string)
}

provider "aws" {
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
  region     = var.AWS_REGION
}

# S3 Bucket Creation
resource "aws_s3_bucket" "pipeline_test_s3_bucket" {
  bucket = var.S3_BUCKET_NAME
  acl    = "private"

  tags = var.S3_BUCKET_TAGS
}

output "s3_bucket_name" {
  value = aws_s3_bucket.pipeline_test_s3_bucket.bucket
}
