terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

variable "do_token" {}
variable "project_name" {}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_project" "project" {
  name = var.project_name
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "random_password" "aiuser_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "digitalocean_droplet" "web" {
  image  = "ubuntu-20-04-x64"
  name   = "slack-agent-B"
  region = "nyc3"
  size   = "s-1vcpu-1gb"
  user_data = <<-EOF
              #!/bin/bash
              # Create server_admin user with sudo access
              useradd -m -s /bin/bash server_admin
              echo "server_admin:${random_password.password.result}" | chpasswd
              usermod -aG sudo server_admin
              
              # Create aiuser
              useradd -m -s /bin/bash aiuser
              echo "aiuser:${random_password.aiuser_password.result}" | chpasswd
              EOF
}

resource "digitalocean_project_resources" "project_resources" {
  project = data.digitalocean_project.project.id
  resources = [
    digitalocean_droplet.web.urn
  ]
}

output "droplet_ip" {
  value = digitalocean_droplet.web.ipv4_address
}

output "root_password" {
  value = random_password.password.result
  sensitive = true
}

output "server_admin_password" {
  value = random_password.password.result
  sensitive = true
}

output "aiuser_password" {
  value = random_password.aiuser_password.result
  sensitive = true
}