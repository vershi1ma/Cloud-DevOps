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
  }
}
