provider "aws" {
    region = "eu-north-1"
    access_key = var.aws_access_key
    secret_key = var.aws_secret_key
}

resource "aws_s3_bucket" "media_bucket" {
    bucket = var.bucket_name
    acl = "private"

    tags = {
        Name        = "Generative AI Media Bucket"
        Environment = "Dev"
    }
}