terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_instance" "cloudlearner_server" {
  ami                    = "ami-07b8fb6bd3e9627a6"
  instance_type          = "t3.micro"
  subnet_id              = "subnet-0f7ad39964643e4b0"
  vpc_security_group_ids = ["sg-01939e0d12fa73610"]
  key_name               = "cloudlearner-key"

  tags = {
    Name          = "Cloudlearner-server"
    "Patch Group" = "Cloudlearner"
    ManagedBy     = "Terraform"
  }
}

resource "aws_s3_bucket" "cloudlearner_website" {
  bucket = "cloudlearner-website-vershi1ma"

  tags = {
    Name      = "Cloudlearner-website"
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket_website_configuration" "cloudlearner_website" {
  bucket = aws_s3_bucket.cloudlearner_website.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "cloudlearner_website" {
  bucket = aws_s3_bucket.cloudlearner_website.id

  block_public_acls       = false
  ignore_public_acls      = false
  block_public_policy     = false
  restrict_public_buckets = false
}
