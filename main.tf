provider "aws" {
  region = "eu-north-1"
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
  owners = ["099720109477"]
}

variable "epc_api_key" {
  description = "EPC API key"
  type        = string
  sensitive   = true
}

variable "os_api_key" {
  description = "OS API key"
  type        = string
  sensitive   = true
}

variable "session_secret_key" {
  description = "Session secret key for Flask"
  type        = string
  sensitive   = true
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = "./.ssh/terraform_rsa"
}

resource "local_file" "public_key" {
  content  = tls_private_key.ssh_key.public_key_openssh
  filename = "./.ssh/terraform_rsa.pub"
}

resource "aws_instance" "app_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  subnet_id              = "subnet-84e2f4fc"
  vpc_security_group_ids = ["sg-00d5a1d67232f43a4"]
  key_name               = "terraform-key"
  user_data = templatefile("${path.module}/cloud-init.yaml.tmpl", {
    instance_name = "hard-to-heat-homes-2.0"
    epc_api_key   = var.epc_api_key
    os_api_key    = var.os_api_key
    session_secret_key  = var.session_secret_key
  })


  tags = {
    Name = "hard-to-heat-homes-2.0"
  }
}