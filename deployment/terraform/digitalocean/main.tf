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
variable "host_name" {
  description = "The name of the host (Droplet)."
  type        = string
}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_project" "project" {
  name = var.project_name
}

resource "random_password" "password" {
  length           = 32
  special          = false
}

resource "random_password" "aiuser_password" {
  length           = 32
  special          = false
}

resource "digitalocean_droplet" "web" {
  image      = "ubuntu-24-04-x64"
  name       = var.host_name
  region     = "nyc3"
  size       = "s-1vcpu-1gb"
  user_data = <<-EOF
              #!/bin/bash

              # Install docker
              sudo apt-get update
              sudo apt-get install -y \
                apt-transport-https \
                ca-certificates \
                curl \
                software-properties-common
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
              sudo apt-get update
              sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
              sudo systemctl enable docker
              sudo systemctl start docker

              # Create server_admin user with sudo access
              useradd -m -s /bin/bash server_admin
              echo "server_admin:${random_password.password.result}" | chpasswd
              usermod -aG sudo,docker server_admin
              
              # Create aiuser
              useradd -m -s /bin/bash aiuser
              echo "aiuser:${random_password.aiuser_password.result}" | chpasswd
              usermod -aG docker aiuser
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

output "server_admin_username" {
  value = "server_admin"
}

output "server_admin_password" {
  value      = random_password.password.result
  sensitive  = true
}

output "aiuser_password" {
  value      = random_password.aiuser_password.result
  sensitive  = true
}
