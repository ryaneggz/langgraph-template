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
  length           = 32
  special          = false
}

resource "digitalocean_droplet" "web" {
  image  = "ubuntu-20-04-x64"
  name   = "slack-agent-B"
  region = "nyc3"
  size   = "s-1vcpu-1gb"
  user_data = <<-EOF
            #!/bin/bash

            # Create serveradmin user with sudo access
            NEW_USER="serveradmin"
            PASSWORD="${random_password.password.result}"

            useradd -m -s /bin/bash $NEW_USER
            echo "$NEW_USER:$PASSWORD" | chpasswd
            usermod -aG sudo $NEW_USER

            # Install Docker
            apt-get update
            apt-get install -y apt-transport-https ca-certificates curl software-properties-common
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
            add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
            apt-get update
            apt-get install -y docker-ce
            usermod -aG docker $NEW_USER

            # Install Docker Compose
            curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            chmod +x /usr/local/bin/docker-compose
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

output "serveradmin_password" {
  value = random_password.password.result
  sensitive = true
}